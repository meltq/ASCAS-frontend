import tle
import equation
import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt

satellite_id = 43039
api_key = 'AVZC8R-BJMGXU-RVBHGP-5C1S'


def get_equation(satellite_id, api_key):
    l1, l2 = tle.fetch_tle_data(satellite_id, api_key)

    l2[4] = float(l2[4]) * (10**(-len(l2[4])))
    l2 = [float(x) for x in l2]

    mean_motion = l2[7] * np.pi * 2 * u.rad / u.day
    eccentricity = l2[4] * u.one
    raan = l2[3] * u.deg
    inclination = l2[2] * u.deg
    arg_perigee = l2[5] * u.deg
    mean_anomaly = l2[6] * u.deg

    positions, semi_major_axis, semi_minor_axis = equation.get_orbit(mean_motion, eccentricity, raan, inclination, arg_perigee, mean_anomaly)
    print(f"Ellipse equation in orbital plane: (x / {semi_major_axis.value:.6f})^2 + (y / {semi_minor_axis:.6f})^2 = 1")
    return positions, semi_major_axis, semi_minor_axis


get_equation(satellite_id, api_key)
# # Extract X, Y, Z coordinates for plotting or further analysis
# x_vals = [pos[0].to(u.km).value for pos in positions]
# y_vals = [pos[1].to(u.km).value for pos in positions]
# z_vals = [pos[2].to(u.km).value for pos in positions]
#
# # Plotting in 3D
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(x_vals, y_vals, z_vals, label='Satellite Orbit')
# ax.scatter([0], [0], [0], color='blue', label='Earth', s=100)  # Earth's position at the origin
# #
# ax.set_xlabel('X (km)')
# ax.set_ylabel('Y (km)')
# ax.set_zlabel('Z (km)')
# ax.set_title('Satellite Orbit in 3D')
# ax.legend()
# ax.grid(True)
# #
# plt.show()
