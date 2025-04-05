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
    Container for width and shift results from a Griem calculation.

    Takes the real (width) and imaginary (shift) values from the complex results of a griem
    calculation. Provides convenient methods for printing and saving results.

    Arrtributes:
        states (list or np.ndarray): List of upper states.
        width (float or np.ndarray): Stark broadened width.
        shift (float or np.ndarray): Stark broadened shift.
        ratio (float or np.ndarray): Ratio of shift and width.
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


