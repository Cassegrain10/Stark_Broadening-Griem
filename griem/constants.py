# constants.py

# Importing modules
import constantsjm as const


# Map of spectroscopy notation to angular momentum quantum number ℓ values
ANGULAR_MOMENTUM_QUANTUM_NUMBERS = {
    'S': 0,
    'P': 1,
    'D': 2,
    'F': 3,
    'G': 4
}

# Physical constants
SPEED_OF_LIGHT = const.c        # [m/s]
H_BAR = const.hbar              # [J s]
ELECTRON_MASS = const.me        # [kg]
BOLTZMANN_CONSTANT = const.k    # [J/K]