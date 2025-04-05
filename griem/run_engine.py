"""
run_engine.py

Main engine that ties together all submodules for calculating Stark widths and shifts
using the Griem model. This function is called by higher-level interfaces (e.g. Griem API)
and encapsulates the full computation pipeline from raw energy data to final result.
"""

# Import modules
import numpy as np
from typing import Union

from .utils.helpers import load_energy_data
from .calc.data_processing import process_data
from .calc.data_processing import create_terms
from .calc.rho_min.rhos_solve import calculate_rhos
from .calc.summation import sum
from .calc.integral import integrate_griem


# Main function
def run(
        element: str, 
        lower_state: str, 
        upper_state:str, 
        velocity: Union[float, np.ndarray], 
        EVDF: Union[float, np.ndarray] = 1.0, 
        n_terms: int = 1):
    """
    Perform a full Griem line-broadening calculation for a given transition.

    This function loads energy data for the specified element, processes the lower and upper 
    states, creates the perturbing terms, calculates the rho_min values, performs the 
    summation and integration steps, and finally computes the Stark width and shift result.

    Args:
        element (str): The alkali element symbol (e.g. 'Rb').
        lower_state (str): Lower state of the transition (e.g. '4D3/2').
        upper_state (str): Upper state(s) of the transition (e.g. '12F5/2' or 'F5/2').
        velocity (float, np.ndarray): Velocity of the electrons - can be a single value (v_bar),
                                        or it can be an array of velocities used with an EVDF.
        EVDF (float, np.ndarray, optional): Electron velocity distribution function (e.g. 
                                            Maxwell-Boltzmann). Defaults to 1.0.
        n_terms (int, optional): The number of perturbing states to include in the calculation. 
                                    Defaults to 1.

    Returns:
        tuple:
            integral (float): The final integrated line width/shift (Stark broadening contribution).
            interacting_states (list): List of interaction state labels used in the calculation.
            processed_data (pd.DataFrame): Processed energy and transition data used in the summation.
    """
    # Perform calculation pipelining
    data = load_energy_data(element)
    processed_data = process_data(data, lower_state, upper_state)
    omegas, exp_vals_sqrd, interact_states = create_terms(processed_data, n_terms)
    rhos = calculate_rhos(velocity, omegas, exp_vals_sqrd)
    summation = sum(rhos, velocity, omegas, exp_vals_sqrd)
    integral = integrate_griem(velocity, rhos, summation, EVDF) / (2*np.pi)
    return integral, interact_states, processed_data





