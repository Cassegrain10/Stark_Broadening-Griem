"""
rhos_solve.py

Solves for all critical impact parameters (rho_min) across a range of electron velocities.

This module loops over an array of electron velocities and numerically solves the
rho_min equation for each using a specified root-finding method. These values are used
in the Griem model to describe electron impact line broadening.
"""

# Import modules
import numpy as np

from ...calc.rho_min.rho import rho_equation
from ...calc.rho_min.root_solver import solve

# Main equation
def calculate_rhos(
        vels: np.ndarray, 
        omegas: np.ndarray, 
        exp_vals_sqrd: np.ndarray
    ):
    """
    Solve for rho_min across a range of electron velocities.

    For each velocity in `vels`, this function solves the rho_min equation using
    a root-finding method over a fixed bracketed domain. It returns an array of 
    rho_min values corresponding to each input velocity.

    Args:
        vels (np.ndarray): Electron velocities. Can be a scalar or array-like.
        omegas (np.ndarray): Angular frequency differences between upper and perturbing states.
        exp_vals_sqrd (np.ndarray): Squared matrix elements for each interacting state.

    Returns:
        np.ndarray: Array of rho_min values, one for each electron velocity.
    """
    vels = np.atleast_1d(vels)
    rhos = np.empty_like(vels, dtype=np.float64)
    domain = [0.01, 1e+8]

    for vel, n in zip(vels, range(0, len(vels))):
        rho = solve(rho_equation, domain, vel, omegas, exp_vals_sqrd)
        rhos[n] = rho
    return rhos

