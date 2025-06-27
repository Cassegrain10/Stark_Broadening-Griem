from griem import Griem

# Instantiate the Griem class
stark = Griem(element='Rb',
              lower_state = '4D3/2',
              upper_state = '15F5/2',
              velocity = 4.5e5)

# Perform the broadening calculation
stark.calculate(num_terms=4, want_interact_states=True)

# Printing the broadening results for the 4D3/2 -> 15F5/2 transition
stark.results.print()

# Saving the results
stark.results.save("broadening_results.csv")
