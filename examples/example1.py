# Import libraries
from griem import Griem

# Create Griem API
stark = Griem(element="Rb",
              lower_state="4D3/2",
              upper_state="F5/2",
              velocity=4.5e5)
            
# Calculate
stark.calculate(num_terms=1)

# Print and save results
results = stark.results
results.print()
results.save("griem_results_4D-nF.csv")
              