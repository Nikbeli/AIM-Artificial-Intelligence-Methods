# Создаём тензор и перемещаем его на GPU
import torch


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

a = torch.rand(3, 3).to(device)
b = torch.rand(3, 3).to(device)
c = a + b

print("a + b =", c)
print("Вычислено на:", device)