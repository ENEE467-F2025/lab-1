import numpy as np
from spatialmath import *
import matplotlib.pyplot as plt
from math import pi

# type hints
hour = float
kilometer = float
rad = float
degree = float

# constants
r_e: kilometer = 6_378 # Earth radius

def sat_transform(
        t: hour,
        orbital_params: dict
    ) -> SE3:
    """Get the tranformation of a satellite in the ECI frame.

    Args:
        t: Hours since UTC 00:00.
        params: Dictionary of orbital parameters.

    Returns:
        An SE3 transformation matrix representing the current frame.
    """

    epoch = orbital_params["epoch"]
    inclination = np.deg2rad(orbital_params["inclination"])
    height = orbital_params["height"]
    raas = np.deg2rad(orbital_params["raas"])
    revolutions = orbital_params["revolutions"]
    mae = np.deg2rad(orbital_params["mae"])

    w_s = 2*np.pi*revolutions / 24 # rad/hour

    # TODO: Implement this method
    # T = ...
    # return T

def ecef_transform(t: hour) -> SE3:
    """Get the ECEF frame.

    Args:
        t: Hours since UTC 00:00.
    
    Returns:
        The ECEF frame.
    """

    w_e = 2*np.pi/24

    return SE3.Rz(w_e*t)

#

def main():
    
    t_start: hour = 0.5
    t_stop: hour = 2.5
    N = 1000

    t = np.linspace(t_start, t_stop, N)

    # orbital parameters
    params = {
        "epoch": 1.5, # hours UTC
        "inclination": 51.6331, # degrees
        "height": 413, # kilometers
        "raas": 231.5214, # degrees, right ascension of ascending node
        "revolutions": 15.50263553, # orbits per day
        "mae": 27.0500, # degrees, mean anomaly at epoch
    }

    # polar coordinates (lon, lat)
    PC = np.empty((N,2))

    for i in range(N):
        
        # get ECEF and Sat frame in the ECI coordinates
        T_ecef = ecef_transform(t[i])
        T_sat = sat_transform(t[i], params)
        
        # get relative transformation
        # TODO: Compute the relative transformation
        # T = ...

        d = T.t # position of satellite in ECEF frame

        r = np.linalg.norm(d) # magnitude of position vector

        # TODO: Compute the polar coordinates
        # lon = ...
        # lat = ...

        PC[i] = [lon, lat]
    
    atlas = plt.imread("atlas.jpg")
    plt.imshow(atlas, extent=[-np.pi, np.pi, -np.pi/2, np.pi/2], alpha=0.5)
    plt.scatter(PC[:,0], PC[:,1], s=.1, color="red")
    plt.xlabel("LONGITUDE (rad)")
    plt.ylabel("LATITUDE (rad)")
    plt.title("Satellite Coverage")
    plt.show()

if __name__ == "__main__":
    main()