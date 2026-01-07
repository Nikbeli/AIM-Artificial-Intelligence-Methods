import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import SimpleExpSmoothing, Holt, ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt
import os as os
from sklearn.model_selection import TimeSeriesSplit

def exp1():
    np.random.seed(42)
    dates = pd.date_range(start='2010-01-01', end='2023-12-31', freq='M')
    values = np.cumsum(np.random.normal(scale=5, size=len(dates))) + 100
    data = pd.DataFrame({'Date': dates, 'Value': values})
    data.set_index('Date', inplace=True)

    train = data.loc[:'2022-12-31']
    test = data.loc['2023-01-01':]

    lab11(train, test, True, '1')

def exp2():
    np.random.seed(42)
    dates = pd.date_range(start='2010-01-01', end='2023-12-31', freq='M')
    values = np.cumsum(np.random.normal(scale=5, size=len(dates))) + 100
    data = pd.DataFrame({'Date': dates, 'Value': values})
    data.set_index('Date', inplace=True)

    tscv = TimeSeriesSplit(n_splits=5)

    all_metrics = []

    for train_index, test_index in tscv.split(data):
        train = data.iloc[train_index]
        test = data.iloc[test_index]

        fold_metrics = lab11(train, test, True, '2')
        all_metrics.append(fold_metrics)

    avg_metrics = pd.concat(all_metrics).groupby(level=0).mean()
    print("\nСредние метрики качества прогноза по всем фолдам:")
    print(avg_metrics)

    with open(os.getcwd() + '\lab11_results.txt', 'a', encoding='windows-1251') as f:
        f.write("\n\nЭксперимент №2: Средние метрики качества прогноза по всем фолдам:\n")
        f.write(avg_metrics.to_string())
        f.write("\n\n" + "=" * 50 + "\n\n")

def exp3():
    df = pd.read_csv(os.getcwd() + '\coin_Bitcoin.csv', sep=",", encoding="windows-1251")
    data = pd.DataFrame({'Date': df['Date'], 'Value': df['High']})
    data.set_index('Date', inplace=True)

    train = data[data.index <= '2021-01-01']
    test = data[data.index > '2021-01-01']

    lab11(train, test, False, '3')

def exp4():
    df = pd.read_csv(os.getcwd() + '\coin_Bitcoin.csv', sep=",", encoding="windows-1251")
    data = pd.DataFrame({'Date': df['Date'], 'Value': df['High']})
    data.set_index('Date', inplace=True)

    tscv = TimeSeriesSplit(n_splits=5)

    all_metrics = []

    for train_index, test_index in tscv.split(data):
        train = data.iloc[train_index]
        test = data.iloc[test_index]

        fold_metrics = lab11(train, test, False, '4')
        all_metrics.append(fold_metrics)

    avg_metrics = pd.concat(all_metrics).groupby(level=0).mean()
    print("\nСредние метрики качества прогноза по всем фолдам:")
    print(avg_metrics)

    with open(os.getcwd() + '\lab11_results.txt', 'a', encoding='windows-1251') as f:
        f.write("\n\nЭксперимент №4: Средние метрики качества прогноза по всем фолдам:\n")
        f.write(avg_metrics.to_string())
        f.write("\n\n" + "=" * 50 + "\n\n")

def exp5():
    df = pd.read_csv(os.getcwd() + '\Данные 136.csv', sep=";", encoding="windows-1251")
    data = pd.DataFrame({'Date': df['date'], 'Value': df['totalNumberCreate']})
    data.set_index('Date', inplace=True)

    train = data[data.index <= '1.03.2025  1:30:00']
    test = data[data.index > '1.03.2025  1:30:00']

    lab11(train, test, True, '5')

def exp6():
    df = pd.read_csv(os.getcwd() + '\Данные 136.csv', sep=";", encoding="windows-1251")
    data = pd.DataFrame({'Date': df['date'], 'Value': df['totalNumberCreate']})
    data.set_index('Date', inplace=True)

    tscv = TimeSeriesSplit(n_splits=5)

    all_metrics = []

    for train_index, test_index in tscv.split(data):
        train = data.iloc[train_index]
        test = data.iloc[test_index]

        fold_metrics = lab11(train, test, True, '6')
        all_metrics.append(fold_metrics)

    avg_metrics = pd.concat(all_metrics).groupby(level=0).mean()
    print("\nСредние метрики качества прогноза по всем фолдам:")
    print(avg_metrics)

    with open(os.getcwd() + '\lab11_results.txt', 'a', encoding='windows-1251') as f:
        f.write("\n\nЭксперимент №6: Средние метрики качества прогноза по всем фолдам:\n")
        f.write(avg_metrics.to_string())
        f.write("\n\n" + "=" * 50 + "\n\n")

def lab11(train, test, labels = True, expN = '0'):

    ses_model = SimpleExpSmoothing(train).fit()
    ses_forecast = ses_model.forecast(len(test))

    holt_model = Holt(train).fit()
    holt_forecast = holt_model.forecast(len(test))

    hw_model = ExponentialSmoothing(train, seasonal_periods=12, trend='add', seasonal='add').fit()
    hw_forecast = hw_model.forecast(len(test))

    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train['Value'], label='Обучающие данные', color='blue')
    plt.plot(test.index, test['Value'], label='Фактические значения', color='green')
    plt.plot(test.index, ses_forecast, label='Простое сглаживание', color='red', linestyle='--')
    plt.plot(test.index, holt_forecast, label='Метод Холта', color='purple', linestyle='--')
    plt.plot(test.index, hw_forecast, label='Холт-Винтерс', color='orange', linestyle='--')
    plt.title('Прогнозирование временного ряда')
    if labels:
        plt.xticks(rotation=90)
        plt.xlabel('Дата')
    plt.ylabel('Значение')
    plt.legend()
    plt.grid(True)
    plt.show()

    def calculate_metrics(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = sqrt(mse)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        return {'MAE': mae, 'MSE': mse, 'RMSE': rmse, 'MAPE': mape}

    ses_metrics = calculate_metrics(test['Value'], ses_forecast)
    holt_metrics = calculate_metrics(test['Value'], holt_forecast)
    hw_metrics = calculate_metrics(test['Value'], hw_forecast)

    metrics_df = pd.DataFrame([ses_metrics, holt_metrics, hw_metrics],
                              index=['Простое сглаживание', 'Метод Холта', 'Холт-Винтерс'])

    print("\nМетрики качества прогноза:")
    print(metrics_df)

    with open(os.getcwd() + '\lab11_results.txt', 'a', encoding='windows-1251') as f:
        f.write(f"\n\n Эксперимент №{expN} Метрики качества прогноза:\n")
        f.write(metrics_df.to_string())
        f.write("\n\n" + "=" * 50 + "\n\n")

    return metrics_df

if __name__ == "__main__":

    with open(os.getcwd() + '\lab11_results.txt', 'w', encoding='windows-1251') as f:
        pass

    exp1()
    exp2()
    exp3()
    exp4()
    exp5()
    exp6()