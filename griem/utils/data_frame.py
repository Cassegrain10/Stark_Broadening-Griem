"""
data_frame.py

A lightweight wrapper around pandas DataFrames for printing and saving formatted tables.

Adds optional titles, pretty printing with borders, and convenience methods for exporting
to CSV or Excel formats.
"""


# Import modules
import pandas as pd
from tabulate import tabulate
import math

class Table:
    """
    A wrapper class for pandas DataFrames with optional pretty-printing and saving functionality.

    Attributes:
        table (pd.DataFrame): The underlying data to display or export.
        _title (str or None): Optional title used for display and generating default filenames.

    Methods:
        print(): Pretty-print the table with an optional title header.
        save(filename=None): Save the table as a CSV or Excel file in the /output directory.
    """
    def __init__(
            self, 
            df: pd.DataFrame, 
            title: str = None
    ):
        """
        Initialize a Table object.

        Args:
            df (pd.DataFrame): The data to be wrapped and displayed/exported.
            title (str, optional): Optional title used for display and default filename.
        """
        self.table = df
        self._title = title

    def print(self):
        """
        Pretty-print the table with an optional centered title.

        If a title is provided, it is centered above the table with "=" padding.
        The table is printed using the GitHub markdown format via `tabulate`.
        """
        table_tabulated = tabulate(self.table, headers="keys", tablefmt="github", showindex=False)
        
        if self._title is not None:
            table_width = max(len(line) for line in table_tabulated.splitlines())
            side_width = math.ceil((table_width - 13)/2)
            print('='*side_width + self._title + '='*side_width)
        print(table_tabulated)
        print("\n\n\n")

    def save(
            self, 
            filename: str = None
        ):
        """
        Save the table to a file in CSV or Excel format.

        If no filename is provided, a default is generated from the title (if available).

        Args:
            filename (str, optional): Name of the file to save. Must end with '.csv' or '.xlsx'.

        Raises:
            ValueError: If no filename is provided and no title exists, or if the file extension is unsupported.
        """
        if filename is None:
            if self._title is not None:
                filename = self._title.replace(" ", "_").lower() + ".csv"
            else:
                raise ValueError("No filename or title procided for saving.")
            
        if filename.endswith(".csv"):
            self.table.to_csv(f"output/{filename}", index=False)
        elif filename.endswith(".xlsx"):
            self.table.to_excel(f"output/{filename}", index=False)
        else:
            raise ValueError("Filename must end with .csv or .xlsx")
