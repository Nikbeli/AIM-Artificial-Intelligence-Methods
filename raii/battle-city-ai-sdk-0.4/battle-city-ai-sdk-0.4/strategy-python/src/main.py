import grpc
from typing import Iterator
import game_session_base_pb2 as pb2
import game_session_base_pb2_grpc as pb2_grpc
from strategy import Strategy
import os
import time

class GameSessionClient:
    def __init__(self, server_address: str):
        self._server_address = server_address
        self._strategy = Strategy()
        
    def connect(self, strategy_version: int, author_name: str, strategy_uuid: str):
        """Подключение к игровой сессии"""
        with grpc.insecure_channel(self._server_address) as channel:
            stub = pb2_grpc.GameSessionBaseServiceStub(channel)
            
            # Формируем запрос на подключение
            request = pb2.ConnectRequest(
                strategy_version=strategy_version,
                author_name=author_name,
                strategy_uuid=strategy_uuid
            )
            
            # Вызываем метод Connect
            response = stub.Connect(request)
            
            # Передаем ответ стратегии
            self._strategy.on_connect(response)
            
    def _generate_requests(self) -> Iterator[pb2.StrategyReaction]:
        """Генератор запросов для bidirectional streaming"""
        while True:
            try:
                # Блокируемся, пока не получим реакцию из очереди
                reaction = self._strategy._response_queue.get()
                if reaction is None:  # Сигнал для завершения
                    break
                yield reaction
            except Exception as e:
                print(f"Error in request generator: {str(e)}")
                break
    
    def play_session(self):
        """Запуск игровой сессии"""
        if not self._strategy._session_token:
            raise ValueError("Not connected to session. Call connect() first.")
            
        # Создаем канал с метаданными для аутентификации
        metadata = [('authorization', f'Bearer {self._strategy._session_token}')]
        
        with grpc.insecure_channel(self._server_address) as channel:
            stub = pb2_grpc.GameSessionBaseServiceStub(channel)
            
            # Открываем bidirectional поток
            try:
                # Создаем поток для чтения ответов
                response_stream = stub.PlaySession(
                    self._generate_requests(),
                    metadata=metadata
                )
                
                # Обрабатываем входящие сообщения
                for game_state in response_stream:
                    # Передаем состояние игры стратегии
                    self._strategy.on_game_tick(game_state)
                    
            except grpc.RpcError as e:
                print(f"Session ended with error: {e.code()}: {e.details()}")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
            finally:
                # Отправляем сигнал завершения в генератор запросов
                self._strategy._response_queue.put(None)

# Пример использования
if __name__ == "__main__":
    SERVER_ADDRESS = os.getenv("BCA_GAMESESSION_SERVER_URL", "http://localhost:6469")
    STRATEGY_UUID = os.getenv("BCA_STRATEGY_UUID", "00000000-0000-0000-0000-000000000000")
    client = GameSessionClient(SERVER_ADDRESS.replace("http://", ""))
    time.sleep(3)
    client.connect(Strategy.STRATEGY_VERSION, Strategy.AUTHOR_NAME, STRATEGY_UUID)
    client.play_session()
