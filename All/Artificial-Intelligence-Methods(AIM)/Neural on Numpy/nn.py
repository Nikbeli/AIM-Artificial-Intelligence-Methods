# Работа нейронных сетей под капотом.

import matplotlib

# Устанавливаем размер графиков по умолчанию
matplotlib.rcParams['figure.figsize'] = (10.0, 10.0)
from matplotlib import pyplot as plt

import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle # Перемешивание данных
from sklearn.model_selection import train_test_split

# Прогресс-бар для визуализации обучения
from tqdm import tqdm
from IPython import display


# Функция активации
"""Сигмоида переводит любое значение в диапазон (0, 1), что удобно для бинарной классификации.
Производная используется при обратном распространении ошибки (backpropagation)."""
def activation(z, derivative=False):
    if derivative:
        return activation(z) * (1 - activation(z)) # Производная сигмоиды
    else:
        return 1 / (1 + np.exp(-z)) # Сигмоида — классическая функция активации
    

# Функция потерь
"""MSE (Mean Squared Error) — оценивает разницу между истинными и предсказанными значениями"""
def cost_function(y_true, y_pred):
    n = y_pred.shape[1]
    cost = (1./(2*n)) * np.sum((y_true - y_pred) ** 2)
    return cost # Среднеквадратичная ошибка

def cost_function_prime(y_true, y_pred):
    cost_prime = y_pred - y_true
    return cost_prime # Производная MSE

# Реализация многослойной ИНС  
class NeuralNetwork(object):
    # Инициализация сети
    """weights — список весовых матриц для каждого слоя. biases — векторы смещений для каждого слоя.
    size — список с количеством нейронов на каждом слое, например [2, 4, 1] для сети с 2 входами, 1 скрытым 
    слоем из 4 нейронов и 1 выходом."""
    def __init__(self, size, seed=42):
        """Случайное число задаёт начальное состояние генератора случайных чисел"""
        self.seed = seed
        np.random.seed(self.seed) # # Для воспроизводимости
        """Список, где каждый элемент - количество нейронов в слое и создаём матрицу весов """
        self.size = size
        self.weights = [np.random.randn(self.size[i], self.size[i-1]) * np.sqrt(1 / self.size[i-1])
                        for i in range(1, len(self.size))]
        """Список векторов смещения для каждого слоя, кроме входного"""
        self.biases = [np.random.rand(n, 1) for n in self.size[1:]]

    # Прямой проход по сети.
    """Вычисляется линейная комбинация z = W*a + b, затем применяется функция активации.
        Сохраняются пред-активации (z) и активации (a) для последующего обратного прохода."""
    def forward(self, input):
        a = input
        """Сохраняем значения до функции активации, а второе уже после применения"""
        pre_activations = []
        activations = [a]

        for w, b in zip(self.weights, self.biases):
            """Линейная комбинация z = w*a+b - это пред-активация, а затем применяется функция активации релу, тангх, 
            а в нашем случае сигмоида и далее у нас выход модели прогноз. Градиенты вычисляем по весам"""
            z = np.dot(w, a) + b
            a = activation(z)
            pre_activations.append(z)
            activations.append(a)

        return a, pre_activations, activations
    
    # Вычисление градиентов ошибки на каждом слое (дельт).
    """Для последнего слоя: производная функции потерь x производная активации."""
    def compute_deltas(self, pre_activations, y_true, y_pred):
        """Вычисляем дельты - это локальные градиенты оишбки, которые показывают, насколько активации
        повлияли на финальную ошибку. Ниже производная функции потерь и производная функции активации.
        При перемножении = дельта ошибки"""
        delta_L = cost_function_prime(y_true, y_pred) * activation(pre_activations[-1], derivative=True)
        
        """Длина дельт равна числу слоёв за исключением входного """
        deltas = [0] * (len(self.size) - 1)
        deltas[-1] = delta_L

        """Распространяем ошибку назад (обратное распространение ошибки). Каждая дельта умножается на 
        производную активации текущего слоя"""
        for l in range(len(deltas) - 2, -1, -1):
            delta = np.dot(self.weights[l + 1].transpose(), deltas[l + 1]) * activation(pre_activations[l], derivative=True) 
            deltas[l] = delta

        return deltas
    
    # Вычисление градиентов весов и смещений.
    """Вычисляем градиенты весов и смещений на каждом слое.
    dW_l — производная функции потерь по весам, db_l — по смещениям."""
    def backpropagate(self, deltas, pre_activations, activations):
        dW = []
        db = []
        deltas = [0] + deltas

        for l in range(1, len(self.size)):
            """После дельт вычисляем для слоёв градиенты по весам и по смещениям. Цикл по слоям, а далее усреднение градиентов по batch"""
            dW_l = np.dot(deltas[l], activations[l-1].transpose())
            db_l = deltas[l]
            dW.append(dW_l)
            db.append(np.expand_dims(db_l.mean(axis=1), 1))

        return dW, db
    
    def plot_decision_regions(self, X, y, iteration, train_loss, val_loss, train_acc, val_acc, res=0.01):
        X, y = X.T, y.T
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5

        xx, yy = np.meshgrid(np.arange(x_min, x_max, res), 
                             np.arange(y_min, y_max, res))
        
        Z = self.predict(np.c_[xx.ravel(), yy.ravel()].T)
        Z = Z.reshape(xx.shape)

        plt.contourf(xx, yy, Z, alpha=0.5)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.scatter(X[:, 0], X[:, 1], c=y.reshape(-1), alpha=0.2)
        message = 'iteration: {} " train loss: {} : val loss {} " train acc: {} | val acc: {}'.format(iteration, 
                                                                                                      train_loss, 
                                                                                                      val_loss, 
                                                                                                      train_acc,
                                                                                                      val_acc)
        
        plt.title(message)

    
    # Обучение нейронной сети.
    def train(self, X, y, batch_size, epochs, learning_rate, validation_split=0.2, print_every=10, tqdm_=True, plot_every=None):
        history_train_losses = []
        history_train_accuracies = []
        history_test_losses = []
        history_test_accuracies = []

        """Делим данные на тренировочные и валидационные. Перемешиваем данные перед каждой эпохой."""
        x_train, x_test, y_train, y_test = train_test_split(X.T, y.T, test_size=validation_split, )
        x_train, x_test, y_train, y_test = x_train.T, x_test.T, y_train.T, y_test.T 

        if tqdm_:
            epoch_iterator = tqdm(range(epochs))
        else:
            epoch_iterator = range(epochs)

        for e in epoch_iterator:
            if x_train.shape[1] % batch_size == 0:
                n_batches = int(x_train.shape[1] / batch_size)
            else:
                n_batches = int(x_train.shape[1] / batch_size ) - 1

            x_train, y_train = shuffle(x_train.T, y_train.T)
            x_train, y_train = x_train.T, y_train.T

            """Пакетная обработка. Данные разбиваются на мини-батчи."""
            batches_x = [x_train[:, batch_size*i:batch_size*(i+1)] for i in range(0, n_batches)]
            batches_y = [y_train[:, batch_size*i:batch_size*(i+1)] for i in range(0, n_batches)]

            train_losses = []
            train_accuracies = []
            
            test_losses = []
            test_accuracies = []

            dw_per_epoch = [np.zeros(w.shape) for w in self.weights]
            db_per_epoch = [np.zeros(b.shape) for b in self.biases] 
            
            # Цикл по эпохам и батчам
            """Прямой проход → вычисление ошибки → обратное распространение → обновление весов и смещений.""" 
            for batch_x, batch_y in zip(batches_x, batches_y):
                batch_y_pred, pre_activations, activations = self.forward(batch_x)
                deltas = self.compute_deltas(pre_activations, batch_y, batch_y_pred)
                dW, db = self.backpropagate(deltas, pre_activations, activations)
                for i, (dw_i, db_i) in enumerate(zip(dW, db)):
                    dw_per_epoch[i] += dw_i / batch_size
                    db_per_epoch[i] += db_i / batch_size

                batch_y_train_pred = self.predict(batch_x)

                train_loss = cost_function(batch_y, batch_y_train_pred)
                train_losses.append(train_loss)
                train_accuracy = accuracy_score(batch_y.T, batch_y_train_pred.T)
                train_accuracies.append(train_accuracy)

                batch_y_test_pred = self.predict(x_test)

                test_loss = cost_function(y_test, batch_y_test_pred)
                test_losses.append(test_loss)
                test_accuracy = accuracy_score(y_test.T, batch_y_test_pred.T)
                test_accuracies.append(test_accuracy)


            # Обновление весов и смещений
            """Градиентный спуск: веса корректируются в направлении уменьшения ошибки."""
            for i, (dw_epoch, db_epoch) in enumerate(zip(dw_per_epoch, db_per_epoch)):
                self.weights[i] = self.weights[i] - learning_rate * dw_epoch
                self.biases[i] = self.biases[i] - learning_rate * db_epoch

            history_train_losses.append(np.mean(train_losses))
            history_train_accuracies.append(np.mean(train_accuracies))
            
            history_test_losses.append(np.mean(test_losses))
            history_test_accuracies.append(np.mean(test_accuracies))


            # Ведение истории и визуализация
            """Визуализация границ принятия решений в 2D. Отслеживаем метрики (loss/accuracy).
            Если задано plot_every, строится график границ решений."""
            if not plot_every:
                if e % print_every == 0:    
                    print('Epoch {} / {} | train loss: {} | train accuracy: {} | val loss : {} | val accuracy : {} '.format(
                        e, epochs, np.round(np.mean(train_losses), 3), np.round(np.mean(train_accuracies), 3), 
                        np.round(np.mean(test_losses), 3),  np.round(np.mean(test_accuracies), 3)))
            else:
                if e % plot_every == 0:
                    self.plot_decision_regions(x_train, y_train, e, 
                                                np.round(np.mean(train_losses), 4), 
                                                np.round(np.mean(test_losses), 4),
                                                np.round(np.mean(train_accuracies), 4), 
                                                np.round(np.mean(test_accuracies), 4), 
                                                )
                    plt.show()                    
                    display.display(plt.gcf())
                    display.clear_output(wait=True)

        self.plot_decision_regions(X, y, e, 
                                    np.round(np.mean(train_losses), 4), 
                                    np.round(np.mean(test_losses), 4),
                                    np.round(np.mean(train_accuracies), 4), 
                                    np.round(np.mean(test_accuracies), 4), 
                                    )

        history = {'epochs': epochs,
                   'train_loss': history_train_losses, 
                   'train_acc': history_train_accuracies,
                   'test_loss': history_test_losses,
                   'test_acc': history_test_accuracies
                   }
        return history

    # Получение предсказаний
    """Обычный прямой проход без сохранения промежуточных значений.
    Бинарная классификация: значения больше 0.5 — класс 1."""
    def predict(self, a):
        for w, b in zip(self.weights, self.biases):
            z = np.dot(w, a) + b
            a = activation(z)

        predictions = (a > 0.5).astype(int)
        return predictions


"""1. Нет регуляризации (L2/L1), нормализации, Dropout.

2. Поддержка только бинарной классификации (выход один, sigmoid).

3. Функция активации жёстко зашита — нельзя гибко менять (например, ReLU / tanh)."""