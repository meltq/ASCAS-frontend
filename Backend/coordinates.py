from flask import Flask
import requests
from sgp4.api import Satrec, jday
from datetime import datetime

app = Flask(__name__)

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

if __name__ == '__main__':
    try:
        # Manually enter NORAD ID for the satellite
        sat1_id = 43039
        api_key = 'AVZC8R-BJMGXU-RVBHGP-5C1S'

        # Fetch TLE data for the satellite
        tle_data_sat1 = fetch_tle_data(sat1_id, api_key)

        # Split the TLE data into two lines
        tle_line1_sat1, tle_line2_sat1 = tle_data_sat1.strip().splitlines()

        # Print TLE Line 1 and Line 2
        print(f"TLE Line 1: {tle_line1_sat1}")
        print(f"TLE Line 2: {tle_line2_sat1}")

        # Define the time for which you want to calculate positions
        timestamp = datetime.utcnow()

        # Calculate the position of the satellite
        position_sat1 = calculate_position(tle_line1_sat1, tle_line2_sat1, timestamp)

        # Print the calculated position
        print(f"Position of Satellite (NORAD ID: {sat1_id}): {position_sat1}")

    except Exception as e:
        print(f"Error: {str(e)}")
