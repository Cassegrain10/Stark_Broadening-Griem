from griem import Griem       # Simply imports only the Griem class

# Define the transition and conditions
element = 'Rb'                # Choose an element -> either 'Rb' or 'Cs'
lower_state = '4D3/2'         # Choose a lower state 
upper_state = 'F5/2'          # Choose an upper state -> general or specific, e.g. '12F5/2' or 'F5/2'
electron_velocity = 1.0e6

# Initialize the Griem calculation object
stark = Griem(element=element,
              lower_state=lower_state,     
              upper_state=upper_state,
              velocity=electron_velocity)             

# Run the calculation (using default n_terms=1 perturbing state)
stark.calculate(num_terms=1)

# Print the results
stark.results.print()