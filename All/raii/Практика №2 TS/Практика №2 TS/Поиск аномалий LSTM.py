import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import time
import os as os

class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=50, num_layers=1, batch_first=True)
        self.fc = nn.Linear(50, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out.squeeze(-1)

def train_model(model, data_tensor, epochs=100):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    start_time = time.time()

    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        inputs = data_tensor.unsqueeze(0)  # (1, seq_len, 1)
        output = model(inputs)  # (1, seq_len)
        target = data_tensor.squeeze(1)  # (seq_len)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    training_time = time.time() - start_time
    print(f"Время обучения модели: {training_time:.2f} секунд")

def normalize_min_max(series):
    return (series - series.min()) / (series.max() - series.min())

def searchAnom(colname):
    data = df[colname].to_numpy()
    data = normalize_min_max(data)
    data_tensor = torch.FloatTensor(data).view(-1, 1)

    model = LSTMModel()
    train_model(model, data_tensor)

    model.eval()
    with torch.no_grad():
        reconstructed = model(data_tensor.unsqueeze(0)).squeeze().numpy()

    error = np.abs(reconstructed - data)
    threshold = np.percentile(error, 80)
    anomalies_detected = error > threshold

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(data, marker='o', label='Данные')

    ax.scatter(
        np.where(anomalies_detected)[0],
        data[anomalies_detected],
        color='red',
        label='Аномалии',
        s=100
    )

    ax.set_title(f"Данные и аномалии ({colname})")
    ax.set_xlabel("Индекс")
    ax.set_ylabel("Значение")
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()

df = pd.read_csv(os.getcwd() +  "\Данные 136.csv", sep=";", encoding="windows-1251")

colname = "totalNumberCreate"

plt.figure(figsize=(10, 6))
plt.plot(df[colname], marker='o')
plt.title("График без регистрации аномалий")
plt.grid(True)
plt.show()

searchAnom(colname)