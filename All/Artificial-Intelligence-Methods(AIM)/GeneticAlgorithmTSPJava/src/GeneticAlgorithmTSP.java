import java.util.*;

public class GeneticAlgorithmTSP {

    // Константы для настройки алгоритма
    private static final int NUM_CITIES = 4; // Число городов
    private static final int POPULATION_SIZE = 100; // Размер популяции
    private static final int GENERATIONS = 500; // Количество поколений
    private static final double MUTATION_RATE = 0.1; // Вероятность мутации

    // Матрица расстояний между городами
    private static final int[][] DISTANCES = {
            {0, 10, 15, 25},
            {10, 0, 20, 35},
            {15, 20, 0, 30},
            {25, 35, 30, 0}
    };

    public static void beginAlgorithm() {
        // Инициализация начальной популяции
        List<List<Integer>> population = initializePopulation();
        for (int generation = 0; generation < GENERATIONS; generation++) {
            // Создание нового поколения
            List<List<Integer>> newPopulation = new ArrayList<>();
            while (newPopulation.size() < POPULATION_SIZE) {
                // Выбор родителей
                List<Integer> parent1 = selectParent(population);
                List<Integer> parent2 = selectParent(population);
                // Скрещивание родителей
                List<Integer> child = crossover(parent1, parent2);
                // Применение мутации
                if (Math.random() < MUTATION_RATE) {
                    mutate(child);
                }
                newPopulation.add(child);
            }
            // Замена старой популяции новой
            population = newPopulation;
            // Выбор лучшего маршрута
            List<Integer> bestRoute = getBestRoute(population);
            int bestDistance = calculateDistance(bestRoute);
            System.out.println("Поколение " + generation + ": Лучший маршрут = " + bestRoute + ", Расстояние = " + bestDistance);
        }
    }

    // Инициализация начальной популяции случайными маршрутами
    private static List<List<Integer>> initializePopulation() {
        List<List<Integer>> population = new ArrayList<>();
        for (int i = 0; i < POPULATION_SIZE; i++) {
            List<Integer> route = new ArrayList<>();
            for (int j = 0; j < NUM_CITIES; j++) {
                route.add(j);
            }
            Collections.shuffle(route); // Перемешивание городов
            population.add(route);
        }
        return population;
    }

    // Выбор родителя из популяции
    private static List<Integer> selectParent(List<List<Integer>> population) {
        Random rand = new Random();
        return population.get(rand.nextInt(POPULATION_SIZE));
    }

    // Скрещивание двух родителей для создания потомка
    private static List<Integer> crossover(List<Integer> parent1, List<Integer> parent2) {
        List<Integer> child = new ArrayList<>(Collections.nCopies(parent1.size(), -1));
        Random rand = new Random();
        int start = rand.nextInt(parent1.size());
        int end = rand.nextInt(parent1.size());
        if (start > end) {
            int temp = start;
            start = end;
            end = temp;
        }

        // Копирование части маршрута из первого родителя
        for (int i = start; i <= end; i++) {
            child.set(i, parent1.get(i));
        }

        // Заполнение оставшихся городов из второго родителя
        int childIndex = 0;
        for (int i = 0; i < parent2.size(); i++) {
            int currentCity = parent2.get(i);
            if (!child.contains(currentCity)) {
                while (child.get(childIndex) != -1) {
                    childIndex++;
                }
                child.set(childIndex, currentCity);
            }
        }
        return child;
    }

    // Мутация маршрута
    private static void mutate(List<Integer> route) {
        Random rand = new Random();
        int index1 = rand.nextInt(route.size());
        int index2 = rand.nextInt(route.size());
        Collections.swap(route, index1, index2);
    }

    // Поиск лучшего маршрута в популяции
    private static List<Integer> getBestRoute(List<List<Integer>> population) {
        List<Integer> bestRoute = population.get(0);
        int bestDistance = calculateDistance(bestRoute);
        for (List<Integer> route : population) {
            int distance = calculateDistance(route);
            if (distance < bestDistance) {
                bestRoute = route;
                bestDistance = distance;
            }
        }
        return bestRoute;
    }

    // Расчет расстояния для маршрута
    private static int calculateDistance(List<Integer> route) {
        int distance = 0;
        for (int i = 0; i < route.size() - 1; i++) {
            distance += DISTANCES[route.get(i)][route.get(i + 1)];
        }
        distance += DISTANCES[route.get(route.size() - 1)][route.get(0)]; // Возврат в начальный город
        return distance;
    }
}