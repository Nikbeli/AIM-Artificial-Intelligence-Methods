import game_session_base_pb2 as pb2
import queue
import random
from typing import Dict, Any, List

# --- КОНСТАНТЫ ---
MAP_WIDTH = 15
MAP_HEIGHT = 15
EDGE_THRESHOLD = 1


class Strategy:
    """
    Умная стратегия с параметризованным поведением.
    Может мутировать — подходит для генетического алгоритма.
    """
    STRATEGY_VERSION = 1
    AUTHOR_NAME = "GA Bot"

    def __init__(self, genes: Dict[str, float] = None):
        # Инициализация состояния
        self._session_token = None
        self._team_id = None
        self._map_info = None
        self._units = None
        self._response_queue = queue.Queue()

        # Гены стратегии — определяют поведение
        self.genes = genes.copy() if genes is not None else self._random_genes()

        # Статистика (для оценки после игры)
        self.kills = 0
        self.deaths = 0
        self.damage_dealt = 0
        self.survived_units = 0

    @staticmethod
    def _random_genes() -> Dict[str, float]:
        """Создаёт случайный набор генов"""
        return {
            "move_towards_enemy": random.uniform(0.4, 0.9),
            "shoot_if_enemy_in_range": random.uniform(0.5, 1.0),
            "rotate_towards_closest": random.uniform(0.5, 1.0),
            "avoid_edges": random.uniform(0.6, 0.95),
            "random_move_chance": random.uniform(0.0, 0.3),
            "prefer_closest_target": random.uniform(0.6, 1.0),
        }

    def get_genes(self) -> Dict[str, float]:
        """Возвращает копию генов для ГА"""
        return self.genes.copy()

    def mutate(self, mutation_rate: float = 0.2, strength: float = 0.2):
        """Мутирует гены случайным образом"""
        for key in self.genes:
            if random.random() < mutation_rate:
                self.genes[key] += random.uniform(-strength, strength)
                # Ограничиваем в пределах [0, 1]
                self.genes[key] = max(0.0, min(1.0, self.genes[key]))

    def on_connect(self, connect_reply: pb2.ConnectReply):
        """Обработка подключения к серверу"""
        self._session_token = connect_reply.session_token
        self._team_id = connect_reply.team_id
        self._map_info = connect_reply.map
        self._units = {unit.id: unit for unit in connect_reply.units}

        # Логирование (можно убрать в продакшене)
        print(f"✅ Подключено: Команда {self._team_id}")
        print(f"🗺️  Карта: {self._map_info.width_blocks}x{self._map_info.height_blocks}")
        print(f"👥 Юнитов: {len(self._units)}")

    def on_game_tick(self, game_state: pb2.GameFieldState) -> pb2.StrategyReaction:
        reaction = pb2.StrategyReaction()
        reaction.current_tick = game_state.current_tick

        # Обновляем состояние юнитов
        alive_units = {uid: u for uid, u in self._units.items() if u.is_alive}
        enemies = [
            ent for ent in game_state.entities
            if ent.team != self._team_id and ent.entity_type == pb2.EntityType.UNIT
        ]

        # Размеры карты
        width = self._map_info.width_blocks
        height = self._map_info.height_blocks
        genes = self.genes

        for unit_id, unit in alive_units.items():
            unit_reaction = reaction.units.add()
            unit_reaction.id = unit_id

            x, y = unit.position.x, unit.position.y

            # Поиск ближайшего врага
            closest_enemy_pos = None
            min_dist_sq = float('inf')
            for e in enemies:
                ex, ey = e.position.x, e.position.y
                dist_sq = (ex - x)**2 + (ey - y)**2
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    closest_enemy_pos = (ex, ey)

            # Начальные действия
            target_rotation = pb2.RotationType.NONE
            will_move = False
            will_shoot = False

            # 1. ПОВОРОТ: к ближайшему врагу (с вероятностью)
            if closest_enemy_pos and random.random() < genes["rotate_towards_closest"]:
                dx = closest_enemy_pos[0] - x
                dy = closest_enemy_pos[1] - y
                if abs(dx) >= abs(dy):
                    target_rotation = pb2.RotationType.RIGHT if dx > 0 else pb2.RotationType.LEFT
                else:
                    target_rotation = pb2.RotationType.DOWN if dy > 0 else pb2.RotationType.UP
            else:
                # Случайный поворот (малая вероятность)
                if random.random() < genes["random_move_chance"]:
                    target_rotation = random.choice([
                        pb2.RotationType.UP,
                        pb2.RotationType.DOWN,
                        pb2.RotationType.LEFT,
                        pb2.RotationType.RIGHT
                    ])

            # 2. ДВИЖЕНИЕ: двигаться к врагу?
            if target_rotation != pb2.RotationType.NONE:
                if random.random() < genes["move_towards_enemy"]:
                    will_move = True

            # 3. СТРЕЛЬБА: если враг рядом
            if closest_enemy_pos and min_dist_sq <= 4:  # радиус ~2 клетки
                if random.random() < genes["shoot_if_enemy_in_range"]:
                    will_shoot = True

            # 4. ИЗБЕЖАНИЕ КРАЁВ
            if random.random() < genes["avoid_edges"]:
                if x <= EDGE_THRESHOLD:
                    target_rotation = pb2.RotationType.RIGHT
                    will_move = True
                elif x >= width - EDGE_THRESHOLD:
                    target_rotation = pb2.RotationType.LEFT
                    will_move = True
                elif y <= EDGE_THRESHOLD:
                    target_rotation = pb2.RotationType.DOWN
                    will_move = True
                elif y >= height - EDGE_THRESHOLD:
                    target_rotation = pb2.RotationType.UP
                    will_move = True

            # Применяем действия
            unit_reaction.rotation = target_rotation
            unit_reaction.will_move = will_move
            unit_reaction.will_shoot = will_shoot

        # Помещаем реакцию в очередь (для отправки клиенту)
        self._response_queue.put(reaction)
        return reaction

    def on_game_end(self, game_end: pb2.GameEnd):
        """Сохраняем статистику после игры (для оценки в ГА)"""
        self.kills = game_end.kills
        self.deaths = game_end.deaths
        self.damage_dealt = game_end.damage_dealt
        self.survived_units = len([u for u in self._units.values() if u.is_alive])

    def get_fitness(self) -> float:
        """Возвращает оценку эффективности стратегии"""
        return (
            self.kills * 10 +
            self.survived_units * 8 +
            self.damage_dealt * 0.4 -
            self.deaths * 3
        )