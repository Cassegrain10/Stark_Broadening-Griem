"""
rho_solver.py

Defines the equation used to solve for the critical impact parameter `rho_min`,
which determines the minimum electron-target separation in the Griem line
broadening model. The function returned can be passed to a numerical root solver.

References:
    Griem, H.R. (1956). Physical Review, 102, 1809.
"""


# Import modules
import numpy as np
from scipy.optimize import fsolve, minimize
from scipy.special import gamma

from ...utils.functions import A, B
from ...constants import H_BAR, ELECTRON_MASS


def rho_equation(
        rho: float, 
        vel: float, 
        omegas: np.ndarray, 
        exp_vals_sqrd: np.ndarray
    ):
    """
    Equation to solve for the critical impact parameter (rho_min).

    This function evaluates the left-hand side (LHS) minus the right-hand side (RHS)
    of the equation used to determine `rho_min`, the minimum effective distance for
    collisional interactions between electrons and atoms in the Griem model. It is
    designed to be passed to a root solver (e.g. `scipy.optimize.root_scalar`, `fsolve`, etc.).

    Args:
        rho (float): The trial value of the critical impact parameter (rho_min).
        vel (float): The electron velocity.
        omegas (np.ndarray): Angular frequency differences between upper and perturbing states.
        exp_vals_sqrd (np.ndarray): Squared matrix elements (or transition moments).

    Returns:
        float: The value of the equation LHS - RHS. Root-finding methods will seek
               a value of `rho` for which this function evaluates to zero.
    """
    # Calculate A and B terms
    z_mins = np.abs(1e-10*rho*omegas/vel)
    A_terms, B_terms = np.array(A(z_mins)), np.array(B(z_mins))
    A_sum, B_sum = np.sum(exp_vals_sqrd*A_terms), np.sum(exp_vals_sqrd*B_terms)

    try:
        LHS = (2/3)*((1e+10*H_BAR)/(ELECTRON_MASS*vel*rho))**2*np.sqrt(A_sum**2 + B_sum**2) 
    except ZeroDivisionError:
        LHS = np.inf
    RHS = (1/2*gamma(1/3))**(-3/2)

    # Return difference
    return LHS - RHS

