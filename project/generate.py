import random
import csv

risk_hte = []
risk_hte_path = 'risk_hte.csv'
train_risk = []
val_risk = []
train_risk_path = 'train_risk.csv'
val_risk_path = 'val_risk.csv'

for _ in range(100):
    a = []
    a.append(random.random())  # hohhman transfer
    a.append(random.random())  # risk factor
    a.append((a[0] * 4 * a[1] + a[0]) / 5)
    risk_hte.append(a)
    a = [random.random() for _ in range(10)]  # orbital elements
    b = random.random()  # risk factor
    train_risk.append(a)
    val_risk.append([b])

with open(risk_hte_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(risk_hte)

with open(train_risk_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(train_risk)

with open(val_risk_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(val_risk)
