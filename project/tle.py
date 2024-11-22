import requests
from sgp4.api import Satrec, jday

# Function to fetch TLE data from the API


def fetch_tle_data(norad_id, api_key):
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{norad_id}?apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            tle_data = response.json()['tle']
            tle_line1, tle_line2 = tle_data.strip().splitlines()

            return tle_line1.split(), tle_line2.split()
        except KeyError:
            raise Exception("TLE data not found in the response")
    else:
        raise Exception(
            f"Failed to fetch TLE data. Status Code: {response.status_code}")

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
        raise Exception(
            f"Error in satellite position calculation: {error_code}")
