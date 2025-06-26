"""
griem_results.py


"""

# Import modules
import numpy as np
import pandas as pd
from tabulate import tabulate
from typing import Union

from ..utils.data_frame import Table

# Define main class
class GriemResults():
    """
    Container for Stark width and shift results from a Griem calculation.

    This class extracts and organizes the real and imaginary components of the 
    complex output from a Griem calculation, corresponding to the Stark broadened 
    linewidth (width) and shift, respectively. It provides methods for displaying 
    and exporting the results in a tabular format.

    Attributes:
        states (list or np.ndarray): Upper electronic states corresponding to each result.
        width (float or np.ndarray): Stark broadened linewidths (real part of input).
        shift (float or np.ndarray): Stark line shifts (imaginary part of input).
        ratio (float or np.ndarray): Shift-to-width ratio (d/w) for each state.
        table (Table): A formatted table object for printing and saving results.

    Methods:
        print():
            Prints the formatted results table to the terminal.
        
        save(filename="griem.csv"):
            Saves the results table to a CSV or Excel (.xlsx) file.

    Args:
        width_shift (list or np.ndarray): Complex-valued results from Griem calculation,
                                          where the real part is the width and the imaginary 
                                          part is the shift.
        states (list or np.ndarray): List of upper states for which the calculation was performed.
        interact_states (list or np.ndarray, optional): List of states that contributed to 
                                                        the interaction/broadening for each result.
    """
    def __init__(self, width_shift: Union[list, np.ndarray], 
                 states: Union[list, np.ndarray], 
                 interact_states: Union[list, np.ndarray] = None):
        """Initialize a GriemResults object for storing results.

        Args:
            width_shift (list, np.ndarray): complex result of width/shift calculation/
            states (list, np.ndarray): list of upper states calculation was performed for.
            interact_states (list, np.ndarray, optional): List of interacting states included for
                                                          calculation. Defaults to None.
        """
        # Store arguments as attributes
        self.states = states
        width_shift = np.asarray(width_shift)
        self.width = np.real(width_shift)
        self.shift = np.imag(width_shift)
        self.ratio = None

        # Change to float if only one upper state
        if self.width.size == 1:
            self.width = float(self.width)
            self.shift = float(self.shift)

        # Calculate d/w
        self.ratio = self.shift / self.width

        # Create Table of result data
        table = pd.DataFrame({
            "Upper state": self.states,
            "Width": self.width,
            "Shift": self.shift,
            "d/w":    self.ratio})
        if interact_states is not None:
            table["Interaction states"] = [", ".join(row) for row in interact_states]
        self.table = Table(table, title="Griem Results")

    # Create methods for printing and saving
    def print(self):
        """
        Prints the table to the terminal.
        """
        self.table.print()
        
    def save(self, filename="griem.csv"):
        """
        Saves the table to a csv or xlsx file.

        Args:
            filename (str, optional): Name of saved file. Defaults to "griem.csv".
        """
        self.table.save(filename=filename)


