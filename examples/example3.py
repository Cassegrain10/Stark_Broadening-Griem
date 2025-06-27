
# Import libraries
import numpy as np

from griem import Griem
from griem.constants import H_BAR, ELECTRON_MASS, BOLTZMANN_CONSTANT

# Define Maxwell-Boltz distribution
me = ELECTRON_MASS
kb = BOLTZMANN_CONSTANT

def max_boltz(v: np.ndarray, T: float):
    """
    Computes the Maxwell-Boltzmann speed distribution for electrons at a given temperature.

    Parameters
    ----------
    v : np.ndarray
        Array of speeds (cm/s) at which to evaluate the distribution.
    T : float
        Temperature in Kelvin.

    Returns
    -------
    np.ndarray
        The Maxwell-Boltzmann distribution values evaluated at each speed in `v`.

    Notes
    -----
    The distribution is normalized for electrons and defined as:

        f(v) = (m / (2πkT))^(3/2) * 4πv² * exp(-mv² / (2kT))

    where:
        - m is the electron mass,
        - k is Boltzmann's constant,
        - T is the temperature in Kelvin,
        - v is the speed in cm/s.
    """
    return (me/(2*np.pi*kb*T)**(3/2) * 4*np.pi*v**2 * np.exp(-me*v**2 / (2*kb*T)))

# Define physical parameters, velocity space, and EVDF
T = 500    # [K] temperature

vels = np.linspace(1, 2e6, 100) # velocity space [m/s]
EVDF = max_boltz(v=vels, T=T)   # EVDF

# Normalize just in case :)
area = np.trapezoid(EVDF, vels)
EVDF /= area

# Define the transition and conditions
element = 'Rb'                # Choose an element -> either 'Rb' or 'Cs'
lower_state = '4D3/2'         # Choose a lower state 
upper_state = 'F5/2'          # Choose an upper state -> general or specific, e.g. '12F5/2' or 'F5/2'
electron_velocity = vels      # Velocity space [m/s]
electron_evdf = EVDF          # Maxwellian EVDF

# Initialize the Griem calculation object
stark = Griem(element=element,
              lower_state=lower_state,     
              upper_state=upper_state,
              velocity=electron_velocity,
              EVDF=electron_evdf)             

# Run the calculation (using default n_terms=1 perturbing state)
stark.calculate(num_terms=1)

# Print the results
stark.results.print()