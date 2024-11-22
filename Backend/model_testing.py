import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from sklearn.preprocessing import StandardScaler

# Load the trained model
try:
    model = load_model('satellite_position_model.h5', custom_objects={'mse': MeanSquaredError()})
except Exception as e:
    print("Error loading the model:", e)

# Sample input data: [x, y, z, Vx, Vy, Vz]
sample_data = np.array([1000, 2000, 3000, 0.1, 0.2, 0.3])  # Example values

# Prepare the sample input data
sample_sequence = np.tile(sample_data, (n_steps, 1))

# Normalize the sample data
scaler = StandardScaler()  # Make sure to fit it on your actual training data
sample_sequence_scaled = scaler.fit_transform(sample_sequence)

# Reshape to match model input shape
sample_sequence_reshaped = sample_sequence_scaled.reshape((1, n_steps, 6))

# Function to predict future positions
def predict_next_positions(model, initial_sequence, num_predictions):
    predicted_positions = []
    input_sequence = initial_sequence  # The current sequence of x, y, z, Vx, Vy, Vz
    
    for _ in range(num_predictions):
        pred = model.predict(input_sequence)
        predicted_positions.append(pred[0])
        # Update input sequence by appending the predicted result and shifting the window
        pred_reshaped = np.reshape(pred, (1, 1, 3))  # Predicted shape should match the output size
        input_sequence = np.concatenate((input_sequence[:, 1:, :], np.zeros((1, 1, 6))), axis=1)
        input_sequence[:, -1, :3] = pred_reshaped  # Insert predicted values into the last position
    
    return np.array(predicted_positions)

# Predict next 10 positions
num_predictions = 10
future_positions = predict_next_positions(model, sample_sequence_reshaped, num_predictions)

# Print the predicted future positions
print("Predicted Future Coordinates:")
print(future_positions)
