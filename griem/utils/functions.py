"""
functions.py

This module contains special customs functions from Griem and data filtering helper functions.
"""

# Import modules
import numpy as np
import scipy.special as func

# Define Functions
def A(z):
    """`A(z_min)` function from Griem. Uses modified Bessel functions of the second kind
    of order zero and one.
    Parity = even.

    Args:
        z (numpy.dnarray): independent variable

    Returns:
        numpy.ndarray: dependent variable
    """
    arg = np.abs(z)
    f = z**2*(func.kn(1, arg)**2 + func.kn(0, arg)**2)
    return f

def B(z):
    """`B(z_min)` function from Griem. Uses modified Bessel functions of the second kind
    of order zero and one, and modified Bessel functions of the first kind of order zero
    and one.
    Parity = even.

    Args:
        z (numpy.dnarray): independent variable

    Returns:
        numpy.ndarray: dependent variable
    """
    z = np.asarray(z)
    f = np.empty_like(z, dtype=np.float64)

    use_bessel = z < 1e6

    # Compute where z is sufficiently small so as to not overflow bessel functions
    f[use_bessel] = (
        np.pi * z[use_bessel]**2 * 
        (func.kve(0, z[use_bessel]) * func.ive(0, z[use_bessel]) 
         - func.kve(1, z[use_bessel]) * func.ive(1, z[use_bessel]))
    )

    # Use asymptotic limit for sufficiently large z
    f[~use_bessel] = 0.0

    return f



def a(z):
    """`A(z_min)` function from Griem. Uses modified Bessel functions of the second kind
    of order zero and one.
    Parit = even.
    Args:
        z (numpy.dnarray): independent variable

    Returns:
        numpy.ndarray: dependent variable
    """
    arg = np.abs(z)
    f = arg*func.kn(0, arg)*func.kn(1, arg)
    return f

def b(z):
    """`A(z_min)` function from Griem. Uses a modified Bessel function of the second kind
    of order zero, and a modified Bessel function of the first kind of order one.
    Parity = odd.
    Args:
        z (numpy.dnarray): independent variable

    Returns:
        numpy.ndarray: dependent variable
    """
    z = np.asarray(z)
    f = np.empty_like(z, dtype=np.float64)




    use_bessel = z < 1e8
    sign = np.where(z > 0, 1, -1)[use_bessel]
    arg = np.abs(z)[use_bessel]

    # Compute where z is sufficiently small so as to not overflow bessel functions
    f[use_bessel] = np.pi*(0.5 - arg*func.kve(0, arg)*func.ive(1, arg))*sign

    # Use asymptotic limit for sufficiently large z
    f[~use_bessel] = 0.0
    return f