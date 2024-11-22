import csv
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def create_rnn(input_shape):
    model = Sequential()

    # First RNN Block
    model.add(LSTM(32, activation='relu', return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.25))

    # Second RNN Block
    model.add(LSTM(64, activation='relu', return_sequences=False))  # Only need to set `return_sequences=False` for last RNN layer
    model.add(Dropout(0.25))

    # Fully connected layers
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))

    # Output layer for regression
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    return model


input_shape = (10, 1)  # 10 timesteps with 1 feature per timestep

X_train = []
with open('./data/train_risk.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        X_train.append([float(x) for x in row])
y_train = []
with open('./data/val_risk.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        y_train.append([float(x) for x in row])

X_train = np.array(X_train)
y_train = np.array(y_train)
X_val = np.array(X_train[:100])
y_val = np.array(y_train[:100])

model = create_rnn(input_shape)

model.summary()

model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=32)
model.save('risk_factor.keras')
