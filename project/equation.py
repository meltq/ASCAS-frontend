import numpy as np
from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.constants import GM_earth

# Orbital elements
mean_motion = 1.00270383 * np.pi * 2 * u.rad / u.day
eccentricity = 0.0002945 * u.one
raan = 206.8784 * u.deg
inclination = 0.0135 * u.deg
arg_perigee = 5.6523 * u.deg
mean_anomaly = 96.6140 * u.deg


def get_orbit(mean_motion, eccentricity, raan, inclination, arg_perigee, mean_anomaly):
    # Calculate the semi-major axis from mean motion
    mean_motion_rad_s = mean_motion.to(u.rad / u.s).value
    a_meters = (GM_earth.value / mean_motion_rad_s**2)**(1 / 3)  # No units yet

# Apply units to the result
    a = (a_meters * u.m).to(u.km)

# Create the orbit
    orbit = Orbit.from_classical(
        Earth, a, eccentricity, inclination, raan, arg_perigee, mean_anomaly)

# Convert position in perifocal coordinates to ECI coordinates
# We generate points along the orbit using true anomalies
    num_points = 100
    true_anomalies = np.linspace(0, 2 * np.pi, num_points) * u.rad

# Ellipse equation parameters in the orbital plane
    semi_minor_axis = (a * np.sqrt(1 - eccentricity**2)).value

# Print the equation of the ellipse in the orbital plane

# Get position points in ECI coordinates
    return [orbit.propagate(nu / orbit.n).r for nu in true_anomalies], a, semi_minor_axis
