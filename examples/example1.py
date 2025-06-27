# Import libraries
import griem as gm

# Create Griem class with user defined parameters
stark = gm.Griem(element="Rb",
                 lower_state="4D3/2",
                 upper_state="9F5/2",
                 velocity=4.5e5)

# Calculate the stark widths and shifts
stark.calculate()

# Print the results
stark.results.print()