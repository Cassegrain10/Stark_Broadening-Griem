"""
griem.py

Class that wraps around run() from run_engine.py for API
"""

# Import modules
import numpy as np
from typing import Union

from .utils.data_frame import Table
from .utils.helpers import AliasDict

from .utils.helpers import load_energy_data
from .utils.helpers import find_upper_states
from .run_engine import run
from .results.griem_results import GriemResults



# Define main API class
class Griem:
    """
    The main API for the griem calculation.

    The `Griem` class provides a simple API for the calculation of Stark widths and shifts to 
    electron collisionally broadened transitions in Alkalis. The user specifies the alkali, the 
    lower state, the upper state, the velocity, EVDF, and the number of terms to include in the 
    calculation summation (i.e. the number of perturbing states to include in the calculation). 
    For a detailed derivation of the theory, see Physical Review, 125 177, and for experimental
    benchmarks of the theory see Physical Review, 128 515.

    Attributes:
        element (str): The alkali element symbol (e.g. 'Rb').
        lower_state (str): Lower state of the transition (e.g. '4D3/2').
        upper_state (str): Upper state(s) of the transition (e.g. '12F5/2' or 'F5/2').
        velocity (float, np.ndarray): Velocity of the electrons - can be a single value (v_bar),
                                      or it can be an array of velocities used with an EVDF.
        EVDF (float, np.ndarray): Electron velocity distribution function (e.g. Maxwell-Boltzmann).
        n_terms (int): The number of perturbing states to include in the calculation.

        energy_data (Table): The energy data used for the calculation.
        processed_data (AliasDict): Contains all the dataframes of calculation data.
        results (GriemResults): Contains the widths, shifts, and a table of the widths and shifts.

    Methods:
        calculate(): Run the Griem calculation for the provided input.

    Example:
        >>> griem = Griem("Rb", "4D3/2", "12F5/2", 4e5, n_terms=4)
        >>> griem.calculate()
        >>> griem.results.print()

    """
    def __init__(
            self, 
            element: str, 
            lower_state: str, 
            upper_state: str, 
            velocity: Union[float, np.ndarray], 
            EVDF: Union[float, np.ndarray] = 1.0
        ):
        """Initialize a Griem object for line calculations.

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
        """
        # Store arguments as attributes
        self.element = element
        self.lower_state = lower_state
        self.upper_state = upper_state
        self.velocity = velocity
        self.EVDF = EVDF

        # Initialize attributes for storing intermediate and final calculation values
        self.energy_data = Table(load_energy_data(element), title="Energy Data")
        self.processed_data = None
        self.results = None

    # Define a method for the calculation
    def calculate(
            self,
            num_terms: int = 1,
            want_interact_states: bool = False
        ):
        """Performs the Griem calculation using the specified upper states.

        This will calculate the width/shift for a single upper state if a complete quantum state
        is specified (e.g. "12F5/2"), or the width/shift for all the upper states with L_{j}
        specified (e.g. "F5/2").

        Args:
            want_interact_states (bool): user specifies if to show interacting states.
        """
        states = self._get_states()
        width_shift, interact_states, processed_data = self._build_width_shift(states, num_terms)
        self.processed_data = self._assign_processed_data(states, processed_data)
        self.results = self._assign_results(width_shift, states, interact_states, want_interact_states)

    # Define submethods of `calculation()` method
    def _get_states(self):
        """Gets the upper states that the width and shift will be calculated for.

        Returns:
            np.ndarray: an array of strings of the upper state/s.
        """
        if self.upper_state[0].isdigit():
            return np.array([self.upper_state])
        else:
            return find_upper_states(self.element, self.upper_state)

    def _build_width_shift(
            self, 
            states: np.ndarray,
            num_terms: int = 1
        ):
        """Calculates the width and shift of all the `states`.

        Args:
            states (np.ndarray): array of strings of all the upper states for width and shift calc.

        Returns:
            tuple:
                np.ndarray: width/shift complex value.
                np.ndarray: list of interacting states.
                dict: processed energy/exp_val data for each upper states.                                          
        """
        num_states = len(states)
        width_shift = np.zeros(num_states, dtype=np.complex128)
        interact_states = [[] for _ in range(num_states)]
        processed_data = {}
        for n, state in enumerate(states):
            width_shift[n], interact_states[n], processed_data[n] = run(self.element, self.lower_state, 
                                                                        state, self.velocity, self.EVDF, 
                                                                        num_terms)  
        return width_shift, interact_states, processed_data
    
    def _assign_processed_data(
            self, 
            states: np.ndarray, 
            processed_data: dict
        ):
        """Creates alias for each dict key and converts each dataframe to `Table()`.
        
        Takes dict of processed data dataframes and converts each dataframe to a `Table` and creates
        alias key for each Table, e.g. processed_data[0] = processed_data["12F5/2"].

        Args:
            states (np.ndarray): String array of all upper states to calculate width/shift for.
            processed_data (dict): Contains all processed_data dataframes for each upper state.

        Returns:
            dict: A new AliasDict mapping both integer and state name keys to Table objects.
        """

        tables = {n: Table(processed_data[n], title=f"Upper state {state.replace('/', '')} data")
                  for n, state in enumerate(states)}
        aliases = {state: n for n, state in enumerate(states)}
        return AliasDict(tables, aliases=aliases)
    
    def _assign_results(
            self, 
            width_shift: np.ndarray, 
            states: np.ndarray, 
            interact_states: np.ndarray, 
            want_interact_states: bool
        ):
        """Assigns the results of the calculation.

        Args:
            width_shift (np.ndarray): array of the widths and shifts (np.complex128)
            states (np.ndarray): array of upper states (str)
            interact_states (np.ndarray): 2D array of the interacting states 
                                          included in each calculation.
            want_interact_states (bool): if user wants to show the interacting states.

        Returns:
            GriemResults: object containing widths and shifts to display or save.
        """
        if want_interact_states:
            return GriemResults(width_shift, states, interact_states)
        else:
            return GriemResults(width_shift, states)
        

