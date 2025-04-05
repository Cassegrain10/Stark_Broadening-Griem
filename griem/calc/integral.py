"""
integral.py

Performs the velocity-space integration for Stark broadening using equation (1)
from Griem, Physical Review 128, 515 (1962).

The integral combines impact parameter dependence, the velocity distribution
(EVDF), and a summation over perturbing states to compute the total width/shift.
"""

# Import modules
import numpy as np
from typing import Union

from ..constants import H_BAR, ELECTRON_MASS

def integrate_griem(
        vels: Union[float, np.ndarray], 
        rhos: Union[float, np.ndarray], 
        summation: Union[float, np.ndarray], 
        EVDF: Union[float, np.ndarray]
    ):
    """
    Integrate the velocity-dependent broadening expression from the Griem model.

    This function evaluates and integrates the expression from Griem's theory that includes
    impact parameter (rho), velocity (vel), the summation over perturbing states, and the
    electron velocity distribution function (EVDF). If `vels` is a scalar, the expression is
    evaluated directly; if an array, numerical integration is performed using the trapezoidal rule.

    Args:
        vels (float or np.ndarray): Electron velocity (single value or array for EVDF integration).
        rhos (float or np.ndarray): Critical impact parameter(s), one per velocity.
        summation (float or np.ndarray): Summed contribution from perturbing states, same shape as `vels`.
        EVDF (float or np.ndarray): Electron velocity distribution function values (same shape as `vels`).

    Returns:
        float: Result of the evaluated or integrated broadening expression.
    """
    f = EVDF * (np.pi*vels*(rhos*1e-10)**2 + ((4*np.pi)/(3*vels))*(H_BAR/ELECTRON_MASS)**2 * summation)
    if len(f) == 1:
        return f
    else: return np.trapz(f, vels)
