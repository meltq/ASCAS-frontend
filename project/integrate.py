from flask import Flask, request, jsonify
import requests
from sgp4.api import Satrec, jday
from datetime import datetime, timedelta
from flask_cors import CORS
import numpy as np
from astropy import units as u

app = Flask(__name__)
CORS(app)

# Function to fetch TLE data from the API
def fetch_tle_data(norad_id, api_key):
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{norad_id}?apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            tle_data = response.json()['tle']
            return tle_data
        except KeyError:
            raise Exception("TLE data not found in the response")
    else:
        raise Exception(f"Failed to fetch TLE data. Status Code: {response.status_code}")

# Function to calculate satellite position
def calculate_position(tle_line1, tle_line2, timestamp):
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)

    # Convert the timestamp to Julian date
    jd, fr = jday(timestamp.year, timestamp.month, timestamp.day, 
                  timestamp.hour, timestamp.minute, timestamp.second)

    # Compute the satellite's position (x, y, z) in kilometers
    error_code, position, _ = satellite.sgp4(jd, fr)

    if error_code == 0:
        x, y, z = position
        return {'x': x, 'y': y, 'z': z}
    else:
        raise Exception(f"Error in satellite position calculation: {error_code}")

# Function to get the orbital equation (using a simplified approximation)
def get_orbital_equation(tle_line1, tle_line2):
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)
    
    # Extract eccentricity and mean motion for semi-major axis calculation
    eccentricity = satellite.ecco  # Eccentricity
    mean_motion = satellite.no * (60 / (2 * np.pi))  # Mean motion in revs per day

    # Calculate semi-major axis using Kepler's Third Law (approximate)
    mu_earth = 398600.4418  # Earth’s gravitational parameter in km^3/s^2
    semi_major_axis = (mu_earth / (mean_motion * 2 * np.pi / (24 * 3600))**2) ** (1 / 3)  # Semi-major axis in km
    semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity**2)  # Semi-minor axis in km

    return f"(x / {semi_major_axis:.2f})^2 + (y / {semi_minor_axis:.2f})^2 = 1"

@app.route('/api/positions', methods=['POST'])
def get_positions():
    try:
        data = request.json
        sat1_id = data.get('sat1Id')
        sat2_id = data.get('sat2Id')
        api_key = 'AVZC8R-BJMGXU-RVBHGP-5C1S'
        
        # Fetch TLE data for two satellites
        tle_data_sat1 = fetch_tle_data(sat1_id, api_key)
        tle_data_sat2 = fetch_tle_data(sat2_id, api_key)

        # Split the TLE data into two lines
        tle_line1_sat1, tle_line2_sat1 = tle_data_sat1.strip().splitlines()
        tle_line1_sat2, tle_line2_sat2 = tle_data_sat2.strip().splitlines()

        # Define the current time
        current_time = datetime.utcnow()

        # Calculate the current position
        current_position_sat1 = calculate_position(tle_line1_sat1, tle_line2_sat1, current_time)
        current_position_sat2 = calculate_position(tle_line1_sat2, tle_line2_sat2, current_time)

        # Prepare to calculate future positions
        future_positions_sat1 = []
        future_positions_sat2 = []
        future_time_increment = timedelta(minutes=1)  # Increment by 1 minute

        # Calculate positions for the next 10 minutes
        for i in range(1, 11):  # 1 to 10 inclusive
            future_time = current_time + (future_time_increment * i)
            position_sat1 = calculate_position(tle_line1_sat1, tle_line2_sat1, future_time)
            position_sat2 = calculate_position(tle_line1_sat2, tle_line2_sat2, future_time)
            future_positions_sat1.append(position_sat1)
            future_positions_sat2.append(position_sat2)

        # Get the orbital equations
        orbital_equation_sat1 = get_orbital_equation(tle_line1_sat1, tle_line2_sat1)
        orbital_equation_sat2 = get_orbital_equation(tle_line1_sat2, tle_line2_sat2)

        # Return the positions and orbital equations as JSON
        return jsonify({
            'currentPositionSat1': current_position_sat1,
            'currentPositionSat2': current_position_sat2,
            'futurePositionsSat1': future_positions_sat1,
            'futurePositionsSat2': future_positions_sat2,
            'orbitalEquationSat1': orbital_equation_sat1,
            'orbitalEquationSat2': orbital_equation_sat2
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
