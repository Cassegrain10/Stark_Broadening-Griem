"""
helpers.py

Includes helper functions to import energy data, find upper states of a given orbital, and create
a custom dictionary with aliasing of keys.
"""

# Import modules
import os

import numpy as np
import pandas as pd
from collections import UserDict

def load_energy_data(element):
    """
    Imports energy level values for specified alkali.

    Args:
        element (str): user chosen alkali

    Returns:
        pandas.core.frame.DataFrame: Pandas dataframe of Rb energy levels
        with quantum numbers and quantum defect.
    """
    file_map = {
        "Rb": "Rb_energy_values.xlsx",
        "Cs": "Cs_energy_values.xlsx"
    }
    file_name = file_map[element]


    if not file_name:
        ValueError(f"Unsupported element: {element}")

    # Load data into dataframe
    base_dir = os.path.dirname(__file__)  # gets the folder of helpers.py
    file_path = os.path.join(base_dir, "..", "data", file_name)
    file_path = os.path.abspath(file_path)  # clean absolute path
    return pd.read_excel(file_path)


def find_upper_states(element: str, upper_orbital: str):
    """
    Finds all of the upper states with L_{j} in `upper_orbital`.

    Args:
        element (str): The alkali element symbol (e.g. 'Rb').
        upper_orbital (str):  Upper orbital of the transition (e.g. 'F5/2').

    Returns:
        np.ndarray: List of all the upper states with L_{j} momentum.
    """
    data = load_energy_data(element)
    all_states = np.array(data['Config'])
    all_obritals = np.array(data['Config'].str[-4:])
    upper_orbitals_indices = np.where(all_obritals != upper_orbital)[0]
    upper_states = np.delete(all_states, upper_orbitals_indices)
    return upper_states


class AliasDict(UserDict):
    """
    A dictionary subclass that supports aliasing of keys.

    AliasDict behaves like a normal dictionary but allows additional keys ("aliases")
    to refer to the same values as primary keys. This is useful when values should be
    accessible by multiple labels (e.g., by index and by name).

    Attributes:
        aliases (dict): A mapping from alias keys to actual dictionary keys.

    Methods:
        add_alias(alias, key): Add a single alias for an existing key.
        add_aliases(alias_dict): Add multiple aliases from a dictionary.
    """
    def __init__(self, data=None, aliases=None):
        """
        Initialize the AliasDict with optional data and aliases.

        Args:
            data (dict, optional): Initial dictionary data.
            aliases (dict, optional): Initial mapping of aliases to real keys.
        """
        self.aliases = aliases or {}
        super().__init__(data or {})
                
    def __getitem__(self, key):
        """
        Retrieve a value by key or alias.

        Args:
            key (Any): Primary key or alias.

        Returns:
            Any: The value associated with the resolved key.
        """
        actual_key = self.aliases.get(key, key)
        return super().__getitem__(actual_key)
    
    def __setitem__(self, key, item):
        """
        Set a value by key or alias.

        Args:
            key (Any): Primary key or alias.
            item (Any): Value to store.
        """
        actual_key = self.aliases.get(key, key)
        return super().__setitem__(actual_key, item)
    
    def add_alias(self, alias, key):
        """
        Add a single alias for an existing key.

        Args:
            alias (Any): Alias key.
            key (Any): Existing key in the dictionary.
        """
        self.aliases[alias] = key
    
    def add_aliases(self, alias_dict):
        """
        Add multiple aliases using a dictionary.

        Args:
            alias_dict (dict): Dictionary mapping aliases to real keys.
        """
        self.aliases.update(alias_dict)
