import requests
import numpy as np
from astropy import units as u
#import matplotlib.pyplot as plt

def fetch_tle_data(satellite_id, api_key):
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{satellite_id}?apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        tle_data = response.json().get('tle')
        return tle_data.strip().splitlines()
    else:
        raise Exception(f"Failed to fetch TLE data. Status Code: {response.status_code}")

def get_orbit(mean_motion, eccentricity, raan, inclination, arg_perigee, mean_anomaly):
    time = np.linspace(0, 2 * np.pi, 100)
    semi_major_axis = (1 / (mean_motion.to(u.rad / u.day).value**2))**(1/3) * 6371 * u.km  # example calculation
    semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity.value**2)
    
    x = semi_major_axis * np.cos(time)
    y = semi_minor_axis * np.sin(time)
    z = np.zeros_like(x)  # Assuming a 2D orbit for simplification
    
    positions = np.vstack((x, y, z)).T * u.km  # converting to km
    return positions, semi_major_axis, semi_minor_axis

def get_equation(satellite_id, api_key):
    tle_data = fetch_tle_data(satellite_id, api_key)
    
    if len(tle_data) < 2:
        raise Exception("TLE data does not contain enough lines.")
    
    l1 = tle_data[0].strip()  # First line
    l2 = [float(x) for x in tle_data[1].strip().split() if x]  # Second line with filtering

    if len(l2) < 8:
        raise Exception("TLE line does not contain enough numeric data.")

    mean_motion = l2[7] * (2 * np.pi) / 86400 * u.rad / u.s  # Convert mean motion to rad/s
    eccentricity = l2[4] * u.one
    raan = l2[3] * u.deg
    inclination = l2[2] * u.deg
    arg_perigee = l2[5] * u.deg
    mean_anomaly = l2[6] * u.deg

    positions, semi_major_axis, semi_minor_axis = get_orbit(mean_motion, eccentricity, raan, inclination, arg_perigee, mean_anomaly)
    
    print(f"Ellipse equation in orbital plane: (x / {semi_major_axis.value:.6f})^2 + (y / {semi_minor_axis.value:.6f})^2 = 1")
    return positions, semi_major_axis, semi_minor_axis

def calculate_future_positions(positions, time_steps, delta_time):
    future_positions = []
    for i in range(1, time_steps + 1):
        # Calculate future position based on simple circular motion (for simplicity)
        future_position = positions[i % len(positions)] * (1 + 0.01 * i)  # Slightly alter the radius as an example
        future_positions.append(future_position)
    
    return np.array(future_positions) * u.km

# Main Execution
api_key = 'AVZC8R-BJMGXU-RVBHGP-5C1S'
satellite_id = int(input("Enter the satellite NORAD ID: "))  # Taking satellite_id as input

positions, semi_major_axis, semi_minor_axis = get_equation(satellite_id, api_key)

# Calculate future positions
time_steps = 10  # Number of future positions to calculate
delta_time = 1  # Time increment in arbitrary units (for demonstration)
future_positions = calculate_future_positions(positions, time_steps, delta_time)

# Print future positions
print("Future Positions (in km):")
for i, pos in enumerate(future_positions):
    print(f"Position {i+1}: X: {pos[0].to(u.km).value:.2f}, Y: {pos[1].to(u.km).value:.2f}, Z: {pos[2].to(u.km).value:.2f}")



# Uncomment to visualize the orbit
# visualize_orbit(positions, future_positions)
