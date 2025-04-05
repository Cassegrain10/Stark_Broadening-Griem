"""
width_shift.py

Extracts the Stark broadening width and shift from the complex result of the Griem integral.

The result of the integral is a complex value in units of [rad/s]. This module
converts it to linear frequency units [Hz] by dividing by 2π, and returns the result
as a complex number, where the real part is the width and the imaginary part is the shift.
"""


# Import modules
import numpy as np

def width_shift(integral: np.complex128):
    """
    Convert the angular frequency result of the integral to Hz and return as complex value.

    The result from the Griem model integration is in angular frequency units [rad/s]. This
    function converts it to linear frequency units [Hz] by dividing by 2π. The result is a
    complex number where the real part represents the Stark width and the imaginary part 
    represents the Stark shift.

    Args:
        integral (np.complex128): Complex-valued result of the integral, in [rad/s].

    Returns:
        np.complex128: Scaled result in [Hz], where:
            - real part = Stark width
            - imaginary part = Stark shift
    """
    integral_scaled = integral / (2*np.pi)  # convert from [rad/s] to [1/s]
    width_shift = integral_scaled
    return width_shift