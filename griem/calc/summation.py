"""
summation.py

Computes the summation term in Equation (1) of Griem, Physical Review 128, 515 (1962).

This summation incorporates velocity-dependent Bessel-function-based interaction terms
(`a(z)` and `b(z)`) for each perturbing state and is used in the integrand of the 
Stark broadening expression.
"""


# Import modules
import numpy as np

from ..utils.functions import a, b

# Main function
def sum(
        rhos: np.ndarray, 
        vels: np.ndarray, 
        omegas:np.ndarray, 
        exp_vals_sqrd: np.ndarray
    ):
    """
    Evaluate the summation term in Griem's Stark broadening model.

    Computes the complex-valued summation over perturbing states, where each term
    depends on the scaled impact parameter (z_min), expectation values, and special
    functions `a(z)` and `b(z)`. Handles single or multiple velocities for integration.

    Args:
        rhos (np.ndarray): Critical impact parameter(s), one per velocity.
        vels (np.ndarray): Electron velocities (can be single value or array).
        omegas (np.ndarray): Angular frequency differences between upper and perturbing states.
        exp_vals_sqrd (np.ndarray): Squared dipole matrix elements (expectation values) 
                                    for each perturbing transition.

    Returns:
        np.ndarray: Array of complex-valued summation results (same length as `vels`).
    """
    vels = np.atleast_1d(vels)
    sums = np.empty_like(vels, dtype=np.complex128)
    for vel, rho, n in zip(vels, rhos, range(0, len(vels))):
        z_mins = 1e-10*rho*omegas/vel

        a_terms, b_terms = np.array(a(z_mins)), 1j*np.array(b((3/4)*z_mins))
        sums[n] = np.sum(exp_vals_sqrd*(a_terms + b_terms))
    return sums