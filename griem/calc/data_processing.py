"""
data_processing.py

Processes atomic energy level data for use in the Griem line broadening model.

This module handles state filtering, transition frequency calculation,
expectation value computation, and extraction of perturbing states.
"""


# Import modules
import numpy as np
import pandas as pd

from ..constants import ANGULAR_MOMENTUM_QUANTUM_NUMBERS, SPEED_OF_LIGHT


# Define main functions
def process_data(
        energy_data: pd.DataFrame, 
        lower_state: str, 
        upper_state: str
    ):
    """
    Filter and process energy level data for Griem line broadening calculations.

    This function filters the provided energy level dataset to extract only the relevant
    perturbing states (i.e., those with Δl = ±1 relative to the upper state). It calculates 
    transition frequencies, angular frequencies, and dipole interaction cross sections, and
    prepares the data for summation in the line broadening model.

    Args:
        energy_data (pd.DataFrame): Raw energy level data, including configuration, l, j, and energy columns.
        lower_state (str): Configuration string of the lower state (e.g., "5P3/2").
        upper_state (str): Configuration string of the upper state (e.g., "12F5/2").

    Raises:
        ValueError: If the `lower_state` or `upper_state` configuration is not found in the data.

    Returns:
        pd.DataFrame: A processed DataFrame containing:
            - transition frequencies (`nu`, `nu_abs`)
            - angular frequencies (`omega`)
            - squared expectation values (`expectation_value_sqrd`)
            - labeled and filtered interaction states
    """
    shift_direction = -1
    # Define quantum values to use in calculations
    upper_momentum_letter = upper_state[-4]
    upper_momentum_value = ANGULAR_MOMENTUM_QUANTUM_NUMBERS[upper_momentum_letter]

    # Deleting rows of momentum other than `upper_momentum_value`
    data = energy_data.copy()
    data = data.loc[(data['l'] == upper_momentum_value + 1) 
                                        | (data['l'] == upper_momentum_value - 1) 
                                        | (data['Config'] == upper_state)]
    
    # Find row index of states
    lower_state_match = data.index[data['Config'] == lower_state]
    if not lower_state_match.empty:
        lower_state_index = lower_state_match[0]
    else:
        raise ValueError(f"No lower state with configuation: {lower_state}")

    upper_state_match = data.index[data['Config'] == upper_state]
    if not upper_state_match.empty:
        upper_state_index = upper_state_match[0]
    else:
        raise ValueError(f"No upper state with configuation: {upper_state}")





    # Calculate energy differences
    # transition_energy = data.loc[lower_state_index, 'Energy'] - data.loc[upper_state_index, 'Energy']
    # omega_lower_state = 2*SPEED_OF_LIGHT*100*np.pi*wave_number
    data['nu'] = SPEED_OF_LIGHT*100*(data['Energy'] - data.loc[upper_state_index, 'Energy'])*shift_direction
    data['nu_abs'] = np.abs(data['nu'])
    data['omega'] = data['nu']*2*np.pi
    data = data.sort_values('nu_abs')

    # Dropping configurations of multiple j
    data['Config_general'] = data['Config'].str[:-3]
    data = data.drop_duplicates(subset=['Config_general'], keep='first')

    # Calculating cross sections
    cross_sections_minus = ((3/2)*data.loc[data['l'] == upper_momentum_value - 1, 'nnl']
                           *np.sqrt(np.abs((data.loc[data['l'] == upper_momentum_value - 1, 'nnl']**2 
                                            - upper_momentum_value**2) / (4*upper_momentum_value**2 - 1))))
    cross_sections_plus = ((3/2)*data.loc[data['l'] == upper_momentum_value + 1, 'nnl']
                        *np.sqrt(np.abs((data.loc[data['l'] == upper_momentum_value + 1, 'nnl']**2 
                                        - (upper_momentum_value + 1)**2) / (4*(upper_momentum_value + 1)**2 - 1))))

    data.loc[data['l'] == upper_momentum_value-1, 'sigma_minus'] = cross_sections_minus
    data.loc[data['l'] == upper_momentum_value+1, 'sigma_plus'] = cross_sections_plus


    data.loc[data['l'] == upper_momentum_value - 1, 'expectation_value_sqrd'] = (
        upper_momentum_value*(2*upper_momentum_value - 1)*data['sigma_minus']**2)
    
    data.loc[data['l'] == upper_momentum_value + 1, 'expectation_value_sqrd'] = (
        (upper_momentum_value + 1)*(2*upper_momentum_value + 3)*data['sigma_plus']**2)
    
    return data


def create_terms(
        processed_data: pd.DataFrame, 
        n_terms: int
    ):
    """
    Extract the n most significant perturbing terms from the processed data.

    This function selects the top `n_terms` perturbing states (based on frequency ordering),
    extracts their angular frequencies and expectation values, and labels them with signed
    directionality (+ or -) for display purposes.

    Args:
        processed_data (pd.DataFrame): The output of `process_data()`, containing sorted and filtered states.
        n_terms (int): Number of perturbing terms to extract for summation.

    Returns:
        tuple:
            omegas (np.ndarray): Angular frequencies (omega) of the perturbing states.
            exp_vals_sqrd (np.ndarray): Expectation values squared for each perturbing state.
            signed_interact_states (list of str): Labels for perturbing states with sign (e.g., "+5D3/2").
    """
    omegas = np.array(processed_data['omega'].iloc[1:n_terms+1]) 
    exp_vals_sqrd = np.array(processed_data['expectation_value_sqrd'].iloc[1:n_terms+1])

    signs_float = np.sign(omegas)
    signs_str = ["+" if sign > 0 else "-" for sign in signs_float]

    interact_states = processed_data['Config'].iloc[1:n_terms+1].tolist()
    signed_interact_states = [sign + state for sign, state in zip(signs_str, interact_states)]

    return omegas, exp_vals_sqrd, signed_interact_states


