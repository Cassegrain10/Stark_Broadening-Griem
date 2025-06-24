# Stark_Broadening-Griem – Stark Broadening Calculation Engine

## Project Overview and Introduction

Stark_Broadening-Griem is a Python project for calculating the Stark broadening of spectral lines in alkali atoms using Griem’s semi-classical model. It provides a high-level API and computational engine to determine the collisional broadening width and shift of spectral lines caused by electron impacts, based on classical path approximation and impact theory. This tool is designed for scientific use, enabling researchers to estimate line broadening parameters for transitions (currently in Rubidium and Cesium) under given electron velocity distributions.

This project implements Griem’s theory of Stark broadening, allowing users to compute the broadening width (FWHM or HWHM of the spectral line profile) and shift (line center displacement) due to electron collisions. The software wraps the complex physics into a user-friendly interface (`Griem` class) while maintaining a clear separation of tasks in the code. By specifying an alkali element (e.g. Rb or Cs), a spectral line (lower & upper atomic states), and electron velocity parameters, the engine computes the Stark broadening parameters according to Griem’s classical impact approximation. The code is modular and well-documented, making it suitable for integration into plasma modeling workflows or for educational purposes in atomic spectroscopy.

### Key features include:

- **Comprehensive Theory Implementation:** Uses Griem’s model ([Physical Review 125:177 (1962)](https://journals.aps.org/pr/abstract/10.1103/PhysRev.128.515); [128:515 (1962)]) to account for electron-impact broadening with adiabatic corrections and summation over perturbing states.
- **High-Level API:** A `Griem` Python class provides a simple interface to set up calculations (specifying element, states, velocities, etc.) and retrieve results. This shields the user from internal details while offering flexibility.
- **Modular Engine:** The calculation pipeline is broken into clear stages (data loading, state selection, critical parameter solving, summation, integration), each handled by dedicated modules.
- **Output of Width and Shift:** Results include the collisional broadening FWHM (width) and line shift, with the option to see details of contributing perturbing transitions. Output can be printed in tabular form or saved to file for further analysis.
- **Use of Experimental Data:** The engine uses tabulated energy levels and quantum defects for Rb and Cs (provided in Excel files) to ensure realistic transition frequencies and matrix elements.
- **Extensible Design:** While currently supporting neutral Rb I and Cs I lines, the structure can be extended to other alkali atoms or refined with additional physical effects in future work.

---

## Quick Start Guide
The rest if this document will be helpful if you want to dig deep into the inner workings if thr code. However, the evst way to learn is to jusy do it. This Wuidj Start Guide should get you up and running in no time! 

### Installing the Library
The first step is of if course, install the library. This step depends of course on what encironment you are using Griem in: cloud-based in *Google Collab*, or locally in Python on your device. 

#### Option 1: Cloud-Based on Google Collab
At the very beginning of your notebook, you will include this,
```python
# Importing `Stark_Broadening-Griem` library into environment
!pip install git+https://github.com/Cassegrain10/Stark_Broadening-Griem.git
```

#### Option 2: Locally in Python
##### Step 1: Install Python
If you don't have Python installed yet...  
- You can download from the [official Python website](https://www.python.org/downloads/) and run from the terminal; however, I would highly reccomend downlaoding [Anaconda](https://www.anaconda.com/download). Anaconda provides terminals to manage your packages in as well as access to Spyder and VS Code (my recomendation).
- Make sure to check **"Add Python to PATH"** during installation.

##### Create a Virtual Environment (Recommended)
A virtual environment keeps your project dependencies isolated and is in general good practice. You must be in your virtual environmnet to access any of the libraries you have `pip install`-ed.  
Open a terminal (Command Prompt on Windows, or you can access through Anaconda Navigator -> CMD.exe prompt) and run:
```bash
python -m venv myenv
```
This will create a virtual environment names `myenv`. Then activate the environment:
- On **Windows**:
  ```bash
  myenv\Scripts\activate
  ```
- On **Mac/Linux**:
  ```bash
  source myenv/bin/activate
  ```
In your terminal you should see something like this if your virtual environment is active:
```
(myenv) $
```

##### Step 3: Install the Library  
With the virtual environmnet active, run:
```bash
pip install git+https://github.com/your-username/your-repo.git
```
**Remember**: You will have to make sure your virtual environment is active every time you want to access a library you have installed inside it.

You now have the library installed!

### Using the Library
Now we will go over several examples on how to use the library.

#### Example 1: Getting Familiar with the Library
If you are using a local version of Python, you can begin with the next step, but remember - if you are using an online environment like Google Collab, you will need to begin your script _every time_ with the above installation instructions for Google Collab.  

1. Import the library - this imports the library into your current script/notebook:
```python
# Import libraries
import griem as gm
```
This imports `griem` and names it `gm`. Now to access an attribute, let's say MyFunc() in the `griem` library, just use `gm.MyFunc().

2. Instantiate an instance of the `Griem` class:
```python
# Create Griem class with user defined parameters
stark = gm.Griem(element="Rb",
                 lower_state="4D3/2",
                 upper_state="9F5/2",
                 velocity=4.5e5)
```
This creates the Griem class - that UI that you will be working with! This sets up the parameters that you want. To perform the calculation,
```python
# Calculate the stark widths and shifts
stark.calculate()
```
The calculations have been performed. Now all that is left is to display them!
```python
# Print the results
stark.results.print()
```

You should see something like this:
```bash
=======================Griem Results=======================
| Upper state   |       Width |        Shift |       d/w |
|---------------|-------------|--------------|-----------|
| 9F5/2         | 5.88916e-10 | -2.09973e-10 | -0.356542 |
```

#### Example 2: Getting to Know the `Griem` Class
Let's get a little more familiar with the Griem class.
```python
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
```

```
=======================Griem Results=======================
| Upper state   |       Width |        Shift |       d/w |
|---------------|-------------|--------------|-----------|
| 4F5/2         | 1.40488e-12 |  8.40408e-13 |  0.598205 |
| 5F5/2         | 1.50602e-11 | -4.03348e-12 | -0.267823 |
| 6F5/2         | 4.75402e-11 | -1.29311e-11 | -0.272004 |
| 7F5/2         | 1.0736e-10  | -2.90627e-11 | -0.270703 |
| 8F5/2         | 2.08105e-10 | -5.52197e-11 | -0.265345 |
| 9F5/2         | 3.61459e-10 | -9.46651e-11 | -0.261897 |
| 10F5/2        | 5.85655e-10 | -1.51066e-10 | -0.257943 |
| 11F5/2        | 8.98192e-10 | -2.28529e-10 | -0.254432 |
| 12F5/2        | 1.3171e-09  | -3.3161e-10  | -0.251773 |
| 13F5/2        | 1.87406e-09 | -4.65236e-10 | -0.24825  |
| 14F5/2        | 2.58516e-09 | -6.34858e-10 | -0.245578 |
| 15F5/2        | 3.49928e-09 | -8.46208e-10 | -0.241824 |
| 16F5/2        | 4.58866e-09 | -1.10583e-09 | -0.240993 |
| 17F5/2        | 5.94347e-09 | -1.42016e-09 | -0.238945 |
| 18F5/2        | 7.57743e-09 | -1.79643e-09 | -0.237076 |
| 19F5/2        | 9.52035e-09 | -2.2422e-09  | -0.235516 |
| 20F5/2        | 1.18356e-08 | -2.76534e-09 | -0.233647 |
| 21F5/2        | 1.44856e-08 | -3.37469e-09 | -0.232969 |
| 22F5/2        | 1.75892e-08 | -4.07872e-09 | -0.231888 |
| 23F5/2        | 2.1147e-08  | -4.88687e-09 | -0.23109  |
| 24F5/2        | 2.51893e-08 | -5.80886e-09 | -0.230609 |
| 25F5/2        | 2.96823e-08 | -6.85487e-09 | -0.230941 |
| 26F5/2        | 3.50845e-08 | -8.0803e-09  | -0.230309 |
| 27F5/2        | 4.1084e-08  | -9.41707e-09 | -0.229215 |
| 28F5/2        | 4.78315e-08 | -1.09137e-08 | -0.22817  |
| 29F5/2        | 5.53814e-08 | -1.25808e-08 | -0.227167 |
| 30F5/2        | 6.38013e-08 | -1.44322e-08 | -0.226206 |
| 31F5/2        | 7.31593e-08 | -1.64817e-08 | -0.225284 |
| 32F5/2        | 8.35202e-08 | -1.87418e-08 | -0.224398 |
| 33F5/2        | 9.49511e-08 | -2.12258e-08 | -0.223544 |
| 34F5/2        | 1.07536e-07 | -2.39507e-08 | -0.222723 |
| 35F5/2        | 1.21348e-07 | -2.69309e-08 | -0.221931 |
| 36F5/2        | 1.36445e-07 | -3.01765e-08 | -0.221163 |
| 37F5/2        | 1.53047e-07 | -3.37371e-08 | -0.220435 |
| 38F5/2        | 1.71051e-07 | -3.75838e-08 | -0.219723 |
| 39F5/2        | 1.9057e-07  | -4.17403e-08 | -0.219029 |
| 40F5/2        | 2.11777e-07 | -4.62434e-08 | -0.21836  |
| 41F5/2        | 2.3483e-07  | -5.11267e-08 | -0.217718 |
| 42F5/2        | 2.59625e-07 | -5.63614e-08 | -0.217088 |
| 43F5/2        | 2.86345e-07 | -6.19867e-08 | -0.216476 |
| 44F5/2        | 3.15135e-07 | -6.80322e-08 | -0.215883 |
| 45F5/2        | 3.46435e-07 | -7.45951e-08 | -0.215322 |
```

Notice how here because we didn't specify the complete upper state, we got all the transitions, 4D3/2 -> nF5/2.  

#### Example 3: Deeper into EEDFs
Notice that in the previous two examples we only gave on value for the electron's velocity, and we provided no EVDF! We specify this as follows:

```python

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
```

_Terminal:_

```
=======================Griem Results=======================
| Upper state   |       Width |        Shift |       d/w |
|---------------|-------------|--------------|-----------|
| 4F5/2         | 6.11639e-13 |  9.90407e-13 |  1.61927  |
| 5F5/2         | 3.16505e-11 | -2.55661e-11 | -0.807763 |
| 6F5/2         | 9.64463e-11 | -7.99597e-11 | -0.829059 |
| 7F5/2         | 2.20206e-10 | -1.81108e-10 | -0.822448 |
| 8F5/2         | 4.46609e-10 | -3.55094e-10 | -0.795089 |
| 9F5/2         | 7.98651e-10 | -6.20879e-10 | -0.77741  |
| 10F5/2        | 1.33796e-09 | -1.01295e-09 | -0.757087 |
| 11F5/2        | 2.11363e-09 | -1.56201e-09 | -0.739014 |
| 12F5/2        | 3.16954e-09 | -2.29894e-09 | -0.725323 |
| 13F5/2        | 4.64514e-09 | -3.28501e-09 | -0.707193 |
| 14F5/2        | 6.55245e-09 | -4.54385e-09 | -0.693459 |
| 15F5/2        | 9.1508e-09  | -6.16954e-09 | -0.674208 |
| 16F5/2        | 1.20825e-08 | -8.09476e-09 | -0.669955 |
| 17F5/2        | 1.59171e-08 | -1.04972e-08 | -0.659492 |
| 18F5/2        | 2.06078e-08 | -1.33943e-08 | -0.649964 |
| 19F5/2        | 2.62255e-08 | -1.68376e-08 | -0.642029 |
| 20F5/2        | 3.31056e-08 | -2.09407e-08 | -0.632544 |
| 21F5/2        | 4.07425e-08 | -2.56316e-08 | -0.629112 |
| 22F5/2        | 4.99086e-08 | -3.11255e-08 | -0.623649 |
| 23F5/2        | 6.03939e-08 | -3.74214e-08 | -0.619621 |
| 24F5/2        | 7.22193e-08 | -4.45734e-08 | -0.617195 |
| 25F5/2        | 8.48719e-08 | -5.25249e-08 | -0.618872 |
| 26F5/2        | 1.00833e-07 | -6.2082e-08  | -0.615689 |
| 27F5/2        | 1.19125e-07 | -7.26882e-08 | -0.610184 |
| 28F5/2        | 1.39863e-07 | -8.46084e-08 | -0.604937 |
| 29F5/2        | 1.63249e-07 | -9.7936e-08  | -0.599916 |
| 30F5/2        | 1.89523e-07 | -1.12788e-07 | -0.595115 |
| 31F5/2        | 2.18928e-07 | -1.29281e-07 | -0.590519 |
| 32F5/2        | 2.51704e-07 | -1.47526e-07 | -0.586109 |
| 33F5/2        | 2.88102e-07 | -1.67638e-07 | -0.58187  |
| 34F5/2        | 3.2842e-07  | -1.89761e-07 | -0.5778   |
| 35F5/2        | 3.72932e-07 | -2.1402e-07  | -0.573884 |
| 36F5/2        | 4.21872e-07 | -2.40509e-07 | -0.570099 |
| 37F5/2        | 4.75925e-07 | -2.69619e-07 | -0.566516 |
| 38F5/2        | 5.34895e-07 | -3.01154e-07 | -0.563014 |
| 39F5/2        | 5.99182e-07 | -3.35309e-07 | -0.559611 |
| 40F5/2        | 6.69348e-07 | -3.72383e-07 | -0.556337 |
| 41F5/2        | 7.45934e-07 | -4.12654e-07 | -0.553204 |
| 42F5/2        | 8.28744e-07 | -4.5592e-07  | -0.550134 |
| 43F5/2        | 9.18391e-07 | -5.02503e-07 | -0.547156 |
| 44F5/2        | 1.01538e-06 | -5.5265e-07  | -0.544276 |
| 45F5/2        | 1.12108e-06 | -6.07132e-07 | -0.541562 |
```
## Theoretical Background: Stark Broadening and Griem’s Model

Stark Broadening refers to the broadening (and shift) of spectral lines due to the presence of electric fields, typically from charged particles in a plasma. Rapid collisions with electrons (and ions) perturb the energy levels of emitting/absorbing atoms, causing spectral lines to widen (broaden) and their centers to shift. In a dense plasma, the cumulative effect of many fleeting collisions produces a Lorentzian line profile characterized by a half-width (or full width at half maximum, FWHM) and a shift of the line center. Griem’s model provides a semi-classical framework to calculate these parameters for electron-impact broadening, treating collisions in the *impact approximation* (assuming sufficiently high perturber density such that collisions are frequent but short compared to radiative timescales).

H. R. Griem’s theory (developed in the 1950s–60s) uses the classical path approach for perturbers: an electron is assumed to travel on a straight-line (classical) trajectory past the radiator, and the cumulative phase perturbation on the radiative transition is computed. Key elements of the model include accounting for deviations from adiabaticity (i.e. non-negligible energy exchange in close collisions) and summing over all possible final states that the transition’s levels can couple to during collisions. Griem’s approach was originally formulated for neutral helium and extended to other elements; it combines classical collision dynamics with quantum mechanical matrix elements for dipole transitions.

In Griem’s impact broadening theory, the Stark width $\Delta\nu_{1/2}$ and shift $\Delta\nu_{\text{shift}}$ are obtained from an integration over the electron velocity distribution and a summation over contributing atomic states. The core formula (referenced as Equation (1) in Griem 1962) involves an integral over impact parameters and electron velocities. The contribution of a given perturbing state is expressed via functions $a(z)$ and $b(z)$, which arise from integrals of Bessel functions (related to the oscillatory phase factors in the impact parameter integration). The real part (involving $a(z)$) contributes to the broadening width, while the imaginary part (involving $b(z)$) contributes to the line shift. These functions encapsulate how a single collision’s effect depends on the collision velocity and the energy separation (frequency $\omega$) between the initial level and a perturbing level. The model introduces a critical impact parameter $\rho_{\min}$ for each collision, essentially the cutoff distance beyond which the perturbation is too weak to affect the line significantly (often related to Debye shielding or validity of impact assumption). Griem’s theory solves for $\rho_{\min}$ by equating the strength of collision perturbation to a threshold condition, a procedure originally outlined in Griem (1956) (Phys. Rev. 102:1809).

### Velocity integration and distribution

The broadening is calculated by integrating over the electron velocity distribution (EEDF/EVDF). In this code, a user-specified distribution is incorporated by weighting each velocity’s contribution. For a Maxwellian electron gas at temperature $T$, a Maxwell-Boltzmann distribution for speeds can be used. The model integrates the product of collision cross-section (impact broadening effect at a given $v$) and the velocity distribution $f(v)$ over all velocities. If a discrete set of velocities with corresponding probabilities is provided, the integration is performed via numerical quadrature (trapezoidal rule).

### Outputs – Width and Shift

The result of the integration is a complex number proportional to the line profile’s complex Lorentzian damping constant, where the real part is the FWHM (width) and the imaginary part is the shift (both in frequency units). In this implementation, the computed complex broadening parameter (initially in angular frequency [rad/s]) is converted to linear frequency [Hz] by dividing by $2\pi$. The width is typically reported as the full width at half maximum (FWHM) of the spectral line (in Hz or in wavelength units via conversion), and the shift is the displacement of the line center (also in Hz or corresponding wavelength). Note that in many cases the shift is much smaller than the width (often a shift/width ratio on the order of 0.1 or less). The code also provides the ratio for easy assessment.

### Accuracy and validity

Griem’s semi-classical model is known to provide order-of-magnitude estimates with reasonable accuracy (often within 20% of experimental values for widths) for a wide range of conditions. It accounts for electron broadening primarily; quasi-static ion broadening is handled via separate assumptions (in this code, ions are not explicitly included except through the cutoff criterion). The model performs well for moderately strong interactions but can deviate at very high densities or for very high principal quantum numbers where full quantum or more refined models (e.g. quantum mechanical line shape codes) might be needed. Nonetheless, Griem’s formulas (and subsequent refinements in his 1974 monograph) have been a cornerstone in plasma spectroscopy, and this project implements those formulas to facilitate quick calculations of Stark broadening parameters.

## Software Structure and Key Modules  
The project is organized as a Python package named `griem`, with modules corresponding to each stage of
the calculation pipeline. The code is written with clarity in mind, using descriptive names and docstrings
that reference the theoretical equations. Below is a breakdown of the key components and their roles:
- **High-Level API (`griem.api`):**  
The `api.py` module defines the main `Griem` class, which is the user-facing interface. This class wraps the entire computation. Users instantiate a Griem object with the desired parameters (element, lower and upper states, etc.), and then call its `calculate()` method to perform the calculation. The `Griem` class handles input validation, calls the underlying engine, and returns results in a structured form. Key attributes include: `element` , `lower_state` , `upper_state` , `velocity` , `EVDF` , and `n_terms` (number of perturbing states to include). The class also stores intermediate data (like processed state data) if needed for inspection. Internally, `Griem.calculate()` invokes the lower-level engine ( run_engine.run ) and wraps the output into a `GriemResults` object (see below).
- **Calculation Engine (`griem.run_engine`):**  
This module (`run_engine.py`) contains the core function `run(element, lower_state, upper_state, velocity, EVDF=1.0, n_terms=1)`. The `run()` function orchestrates the full Stark broadening calculation, step by step:
- **Data Loading:* Uses `utils.helpers.load_energy_data` to read the atomic energy level data
for the specified element. The project includes data files with energy levels and quantum defects for
Rb and Cs.
- State Processing: Calls `calc.data_processing.process_data` to filter relevant states and
compute transition parameters. This function selects the transition of interest (lower and upper
states) and finds all potential perturbing states that could couple to the upper (or lower) level via
dipole-allowed transitions (i.e. states with orbital quantum number $l$ such that $\Delta l = \pm 1$
relative to the upper state). It then computes each such state’s energy difference (transition
frequency $\nu$), the angular frequency $\omega=2\pi\nu$, and the dipole matrix element (squared
expectation value) for the coupling. These values form the basis for calculating collision strengths.
- **Term Selection:** Uses `calc.data_processing.create_terms` to pick the top `n_terms`
perturbing states from the list (based on some significance criterion, typically the smallest energy
detuning or largest oscillator strength). If `n_terms=1` (default), it will choose the single most
significant perturbing transition (often the one closest in energy to the upper level, either above or
below, as that tends to dominate the broadening). If `n_terms` is larger, it will include additional
states (the function labels them with a “+” or “–” sign to indicate whether they lie above or below the
reference transition in energy for clarity in output). This yields a filtered DataFrame of the perturbing
terms with their frequencies and matrix elements.
- **Critical Impact Parameter Calculation:** Calls `calc.rho_min.rhos_solve.calculate_rhos` to
compute $\rho_{\min}$ for each relevant electron velocity. This module sets up the equation for $
\rho_{\min}$ based on Griem’s criterion and uses a root-finding method to solve it numerically.
Essentially, for each electron velocity $v$, it finds the impact parameter $\rho$ at which the collision
is “just adiabatic enough” to no longer significantly perturb the radiator. This $\rho_{\min}(v)$ acts as
an upper limit in the integration of collision effects (collisions with impact parameter larger than $
\rho_{\min}$ are too gentle to contribute to broadening). The calculation uses the sum of
contributions (A and B terms) from all included perturbing states in the criterion equation.
- **Summation Over States:** Calls `calc.summation.sum` to evaluate the complex summation term
for the broadening integrand. This function takes the array of $\rho_{\min}(v)$ values, the array of
electron velocities, and the list of perturbing states’ angular frequencies and matrix elements, and
computes $\sum_j [\langle D^2 \rangle_j { a(z_j) + i\,b(z_j) }]$ for each velocity, where $z_j = \omega_j
\rho_{\min}(v)/v$ is a scaled parameter for state j. Here $a(z)$ and $b(z)$ are special functions
defined in `utils.functions` using modified Bessel functions (they correspond to integrals over
the collision impact parameter; $a$ is related to in-phase perturbations contributing to width, and
$b$ (with a factor of 3/4 in the argument per Griem’s formula) to out-of-phase perturbations
contributing to shift). The output is a complex number (or array) for each velocity representing the
summed effect of all chosen perturbing states.
- **Velocity Integration:** Calls `calc.integral.integrate_griem` to perform the integration over
the velocity space. This function multiplies the summation result by the appropriate factors
(including $v$, $\rho_{\min}^2$, etc. as per Griem’s equation) and the electron velocity distribution
(EVDF) and integrates over $v . If the velocity` parameter was given as a single value (and EVDF
as 1.0), no integration is needed (it simply evaluates the expression at that velocity). If an array of
velocities with a corresponding EVDF array is given, it uses the trapezoidal rule to integrate $f(v)$
times the collision-broadening integrand across the range. The output of this step is a single
complex number representing the combined effect of all velocities (at a reference perturber density,
see Input/Output below).
- **Unit Conversion:** The result from the integral is initially in angular frequency units (rad/s). The
engine converts this to linear frequency (Hz) by dividing by $2\pi$ internally (this is done in the
`run()` function for convenience). The complex result (width + i*shift in Hz) is then returned.

Finally, `run_engine.run` returns a tuple `(width_shift, interact_states, processed_data)`.
Here `width_shift` is the complex broadening result (width = Re(part), shift = Im(part)),
`interact_states` is a list or DataFrame of the perturbing state terms actually used in the summation
(for reporting if needed), and `processed_data` is a DataFrame of all initially processed candidate states
(which can be useful for examining which states were considered and their parameters).
- **Result Container (`griem.results`):**
The `results/griem_results.py` module defines the `GriemResults` class, a simple container for the output. When `Griem.calculate()` is called, it returns a `GriemResults` instance. This object stores:
  - `states`: a tuple or list of the main transition states (e.g. `["4D3/2", "12F5/2"]`),
  - `width` : the Stark width (FWHM) in Hz,
  - `shift` : the Stark shift in Hz,
  - `ratio` : the shift-to-width ratio (dimensionless),
  - `interact_states` : (optional) the list of perturbing state labels that were included (with “+”/“–”
notation if applicable).

The GriemResults class provides convenience methods: print() to display the results in a nicely formatted table, and save(filename) to write the results to a CSV or text file. The printing uses the tabulate library via a utils.data_frame.Table helper to align columns and add headers/borders for readability. For example, the output table will list the transition, the computed width and shift (with units), and the shift/width ratio, and if interactive states are requested, it may also list the perturbing states and their contribution summary.
- **Utilities (griem.utils):** Several helper functions live here:  
  - `utils.helpers`: includes `load_energy_data(element)` which reads the Excel data for the given element into a pandas DataFrame. It also has `find_upper_states(element, upper_orbital)` to retrieve all states matching a given orbital (used if the user specifies an upper state by orbital letter only, e.g. "F5/2" meaning “the series of F5/2 states”). Additionally, it defines an `AliasDict` for internal use (allowing dictionary keys to have aliases – e.g. could be used to map input aliases to actual keys, though in this context its usage might be minimal).
  - `utils.functions`: defines the special functions `A(z)`, `B(z)`, `a(z)`, and `b(z)` as per Griem’s formulas. `A(z)` and `B(z)` correspond to certain integrals involving modified Bessel functions $K_\nu$ and $I_\nu$ (used in the $\rho_{\min}$ equation), while the lowercase `a(z)` and `b(z)` are the ones used in the summation for width and shift (these are related to combinations of Bessel functions of the first and second kind, implementing the specific formulas from Griem). These functions are carefully implemented to handle large or small arguments (using asymptotic forms when necessary to avoid numerical overflow).
  - `utils.data_frame`: defines a `Table` class to wrap pandas DataFrames for pretty printing (adding borders, titles, etc.). This is used in the results printing to display the output or any intermediate tables in a clean format.
  - `utils.helpers` also defines physical constants and lookup tables (for example, a dictionary mapping spectroscopic term symbols to angular momentum quantum numbers: S→0, P→1, D→2, F→3, G→4, etc., defined in `constants.py`). Key physical constants used are the speed of light `c`, reduced Planck constant $\hbar$, electron mass `m_e`, and Boltzmann’s constant `k_B`, all in SI units.  

In summary, the codebase is organized to mirror the theoretical steps. Each module corresponds to a logical piece of the computation, which aids in both understanding and testing. For instance, one could test the `rho_min` solver independently by feeding it known values and comparing against analytical benchmarks, or test the summation function with synthetic data to ensure the $a(z)/b(z)$ combination behaves as expected.  

## Installation and Setup
To install and use Stark_Broadening-Griem, you should have Python 3 (3.7 or above recommended). The project is structured as a standard Python package. You can set it up in one of the following ways:   
**A) Using pip (via GitHub):** If the repository is public on GitHub, you can install directly using pip with the repository URL. For example:
```
pip install git+https://github.com/Cassegrain10/Stark_Broadening-Griem.git
```
This will download the package and its requirements automatically.   
**B) From source (manual install):** Download or clone this repository, then navigate into the project directory. 
```
pip install .
```
This will use the provided `setup.py` to install the `griem` package into your environment. Alternatively, you can use `python setup.py` install for a global install, or `pip install -e`. for an editable install (useful if you plan to modify the code).  

The installation will also fetch the required dependencies (see **Dependencies** below). Ensure that the data files (`Rb_energy_values.xlsx` and `Cs_energy_values.xlsx`) remain in the `griem/data/` directory as expected; the package includes them via `MANIFEST.in`.   

**Note:** If you plan to read the Excel data files via Pandas and encounter an issue, you may need to have the `openpyxl` library installed (Pandas uses it to read `.xlsx` files). This is usually installed automatically with Pandas, but if not, install it via `pip install openpyxl`.  

## Usage Examples  
Once installed, you can use the package in your Python code or interactive environment. Below are a few
example use cases demonstrating how to use the API and run the engine. These examples assume you
have imported the necessary classes/functions from the package:

### Example 1: Basic Stark Broadening Calculation for a Single Velocity
Suppose we want to calculate the Stark broadening of the Rubidium line 4D${3/2}$ – 12F${5/2}$ due to electron impacts at a specific electron velocity (or energy). We’ll use a single representative electron speed (for instance, an average thermal speed at a certain temperature) and get the width and shift.
```python
from griem import Griem

# Define the transition and conditions
element = 'Rb'
lower_state = '4D3/2'
upper_state = '12F5/2'
electron_velocity = 1.0e6  # m/s, an example single velocity (roughly corresponding to a certain eV energy)

# Initialize the Griem calculation object
griem_calc = Griem(element, lower_state, upper_state, velocity=electron_velocity)

# Run the calculation (using default n_terms=1 perturbing state)
result = griem_calc.calculate(num_terms=1)

# Print the results
result.print()
```

What’s happening: We imported the `Griem` class and created an instance with the desired parameters.
Here `velocity=1.0e6 m/s` (a single float) and we did not specify `EVDF` , so it defaults to 1.0 (meaning
we treat that velocity as having weight 1 in the integration). We also left `n_terms` as default (1) in the
object, but explicitly passed `num_terms=1` to c`alculate()` for clarity. The `calculate()` call triggers
the engine to load Rb data, find the 4D${3/2}$ and 12F$$, integrate over the single velocity, and produce the
width and shift states, determine the most significant perturbing state (with $\Delta l = \pm1$ relative to
F, likely a D or G state near 12F), solve for $\rho_{\min}$

The `result.print()` will output something like:
```
Transition               Stark Width (Hz)    Stark Shift (Hz)    Shift/Width   
Perturber(s)
4D3/2 -> 12F5/2          8.5e+09             1.2e+09            0.14         
13G7/2 (example)
```
(The above numbers are illustrative; actual results depend on the physics and data.) If `want_interact_states=True` were used in calculate, the output would list the perturbing state(s) considered (with a “+” or “–” sign if applicable). In this case, it might show, for example, that the `13G7/2` state (just an example) was included (perhaps “+13G7/2” meaning the state above the 12F in energy).  

We can also directly access the values in result if we want to use them in further calculations:  

```python
width_Hz = result.width
shift_Hz = result.shift
ratio = result.ratio
```  
These are floats (or complex components) in linear frequency units (Hz). You could convert to other units (e.g., angstroms of wavelength broadening) if needed by using the central wavelength of the transition.  

### **Example 2: Using Multiple Perturbing States (`n_terms` > 1)**
For a more accurate calculation, you may include more perturbing states. Suppose we suspect the first two nearest levels on each side of the upper state significantly contribute. We can set n_terms=2 or 3, etc.:
```python
# Continuing from the previous setup, now include more perturbing states
result2 = griem_calc.calculate(num_terms=2, want_interact_states=True)
result2.print()
```

By setting `num_terms=2` and `want_interact_states=True`, the engine will include the two most significant perturbing states (e.g., one above and one below the upper level, if available). The output table will then explicitly list which states were used. For example:

```Transition               Stark Width (Hz)    Stark Shift (Hz)   Shift/Width  
4D3/2 -> 12F5/2          8.9e+09             1.3e+09           0.15        
Included perturbing states:
  +13G7/2, –11D5/2
```   

This indicates the calculation included (for instance) the 13G${7/2}$ state above and 11D${5/2}$ state below as perturbing transitions in the sum. The slightly different numeric result (8.9e9 Hz vs 8.5e9 Hz earlier) would reflect the influence of that second state.  

### Example 3: Full Velocity Distribution (Maxwellian)
Often one needs the Stark width/shift at a given electron temperature, which means integrating over a Maxwell-Boltzmann velocity distribution rather than using a single velocity. Here’s how you can do that:

```python
import numpy as np
from griem import Griem

# Define transition (e.g., a Cesium line) and plasma conditions
element = 'Cs'
lower_state = '6S1/2'
upper_state = '6P3/2'
Te = 10000  # electron temperature in K

# Prepare a Maxwellian velocity distribution
me = 9.109e-31  # electron mass (kg)
kB = 1.38065e-23  # Boltzmann constant

# We'll sample velocities (for example, 1000 points from 0 to some vmax)
v_max = 3e6  # an upper cutoff for velocity in m/s (approx)
velocities = np.linspace(0, v_max, 1000)  # m/s

# Maxwell-Boltzmann distribution of speeds (one-dimensional)
# f(v) ~ v^2 * exp(- (1/2 m v^2) / (k_B T)) – but for integration we can use the relative shape
distribution = velocities**2 * np.exp(-0.5 * me * velocities**2 / (kB * Te))

# It’s fine to use a relative distribution since the code will integrate; we can normalize or not 
# because any constant factor cancels out in shift/width ratio (for width/shift per density, normalization isn’t critical except for absolute values, see note below).

# Create the Griem object with velocity array and EVDF
calc = Griem(element, lower_state, upper_state, velocity=velocities, EVDF=distribution)
res = calc.calculate(num_terms=1)
res.print()
``` 

In this example, we created a numpy array of velocities and a corresponding array `distribution` with the Maxwellian distribution function values at those velocities. We passed those to `Griem`. The engine will integrate using trapezoidal integration over this array. The output will be the Stark width and shift for the Cs 6S–6P line at 10,000 K electron temperature (assuming an electron density of 1 per volume unit – see **Input/Output** section). A few things to note:  
- We used 1000 velocity points up to an arbitrary cutoff (3e6 m/s). In practice, you should choose a high enough v_max to capture the tail of the Maxwellian (e.g., a few times the thermal speed). The distribution array could also be normalized, but since the integration formula effectively normalizes by dividing by the number density later, an unnormalized shape works for obtaining width/shift per unit density.
The calculation might be slower with 1000 points; you can adjust the number of points for a balance between accuracy and performance.
- We set n_terms=1 for simplicity; you could increase this if needed for accuracy.
The result’s print() will list the width and shift. If you want to include perturbing state details, use want_interact_states=True in calculate(). However, if many states are included, the list might be long.  

### Example 4: Low-Level Engine Usage  
Advanced users might interact directly with lower-level functions. For instance, one could load data and call run_engine.run directly, or even use calc.data_processing functions for custom analysis. This is generally not necessary for typical use, but it’s possible. For example:
```python
from griem import run_engine
from griem.utils.helpers import load_energy_data

data = load_energy_data('Rb')
# (Filter data or inspect it as needed)
result = run_engine.run('Rb', '5S1/2', '5P3/2', velocity=1e6, EVDF=1.0, n_terms=1)

width_shift, interact_states, processed_data = result
print("Width (Hz):", float(width_shift.real))
print("Shift (Hz):", float(width_shift.imag))
```

This bypasses the Griem class and uses the engine function directly. It returns the complex width_shift as well as the DataFrame of all processed candidates and the list of states used. This level of usage might be useful for debugging or extending the code.  

## Input and Output Formats
**Input parameters:** The main inputs to the Stark broadening calculation are:
- `element` (str): The chemical symbol of the alkali element. Currently supported: `"Rb"` (rubidium) and `"Cs"` (cesium). (*The code is designed for alkalis; using an unsupported element will raise an error.*)
- `lower_state` (str): The spectroscopic designation of the lower level of the transition. It should be in the format `"<principal><orbital><J>"`. For example: `"5S1/2"`, `"4D3/2"`, `"12F5/2"`.
- `upper_state` (str): The upper level of the transition. This can be given in full (e.g. `"12F5/2"`), or you can provide only the orbital and $J$ (e.g. `"F5/2"`). If you provide a partial upper state (just the term symbol and J), the code will retrieve all states in the data with that term (F5/2 in this example) and then apply the `n_terms` selection to pick the closest ones. If you provide the full designation with principal quantum number, that state is taken as the upper level of the line, and additional perturbing states (if any) are chosen relative to it.
- `velocity` (float or np.ndarray of floats): The electron velocity information. If a single float is given, the calculation assumes all electrons have that velocity (or you are calculating at that specific impact velocity). If an array is given, it represents a range of electron speeds (in m/s) that will be integrated over.
- `EVDF` (float or array): The Electron Velocity Distribution Function values corresponding to the velocities above. If `velocity` is a single float, `EVDF` can be left at default 1.0 (meaning a single-velocity delta-function). If `velocity` is an array, then `EVDF` should be an array of the same length giving the relative probability density for each velocity. For a Maxwellian distribution, this would be $f(v) \propto v^2 \exp(-m v^2 / 2 k_B T)$ (or the normalized version). The absolute normalization of `EVDF` does not matter for the resulting width/shift per electron density (the integration routine uses the provided values as weights and effectively normalizes by integration).
- `n_terms` (int): The number of perturbing states to include in the summation. Default is 1 (only the nearest perturbing level). Increase this to include more states for better accuracy (especially if the transition of interest has multiple nearby levels). If you set `upper_state` without a principal number (like "F5/2") and choose `n_terms = N`, the code will consider the N lowest energy states of that term as the “upper state” manifold (this is an advanced usage and effectively means you are looking at a grouped line or wondering how a series converges; typically you specify a single upper state).
- (Optional) `want_interact_states` (bool): When calling `calculate()`, if this is True, the returned `GriemResults` will carry the list of included perturbing state labels and the `print()` output will list them. If `False` (default), the results focus only on the numeric width and shift.  

**Units and formats:**
All velocities should be in SI units (m/s). Energies in the data files are in cm<sup>−1</sup> (wavenumbers) internally converted to frequencies (Hz) via the speed of light.
The output width and shift are given in frequency units (Hz). If needed, you can convert these to wavelength units. For example, a width $\Delta\nu$ in Hz can be converted to $\Delta\lambda$ in Å using $\Delta\lambda = (\lambda^2/c)\Delta\nu$, where $\lambda$ is the line’s central wavelength and $c$ is light speed.
The `GriemResults.print()` method formats the numbers in a readable scientific notation with appropriate significant figures. The `save()` method will output a CSV with numeric values which you can further process or plot.


**Understanding output values:** The computed width and shift correspond to the broadening **per unit electron density** (since no specific electron density N<sub>e</sub> was input). In practice, Stark width scales linearly with electron density in the impact regime. Therefore:  
If you want the actual FWHM at a given electron density $N_e$ (in, say, cm<sup>−3</sup> or m<sup>−3</sup>), you should multiply the output width by $N_e$. Similarly, multiply shift by $N_e$ for the actual shift. Be mindful of units (the code outputs frequency width in Hz per m<sup>−3</sup> if $N_e$ is per m<sup>3</sup>).
For example, if the code returns width $=5\times10^9$ Hz (per m<sup>−3</sup>) and you are interested in a plasma with $N_e = 1\times10^{17}$ cm<sup>−3</sup> (which is $1\times10^{23}$ m<sup>−3</sup>), the FWHM would be $5\times10^9 \times 1\times10^{23} = 5\times10^{32}$ Hz – which is enormous in absolute terms, but you’d likely convert to angstroms: using a line around 600 nm (5×10<sup>14</sup> Hz), this width would be on the order of 0.1 nm, just as an illustration.
If you simply want the broadening parameter at a standard density (often Stark broadening tables normalize to $10^{16}$ cm<sup>−3</sup> or similar), you can multiply accordingly.
Always double-check whether the result has been scaled or not when comparing with literature values. 

**Intermediate outputs:** If you need to inspect which states were considered or their parameters (frequencies, matrix elements, etc.), you can access `calc.processed_data` after running `calculate()`. This `DataFrame` contains columns like `nu` (frequency), `omega`, `expectation_value_sqrd`, etc., for all candidate perturbing states, and indicates which were chosen. The `interact_states` attribute (or the printed list) shows the ones actually included in the summation.  

## Limitations and Future Work
While Stark_Broadening-Griem is a powerful tool for calculating Stark broadening in alkalis, there are important limitations to note, as well as opportunities for future enhancements:
- **Element Coverage:** Currently, the package only includes data for Rubidium (Rb I) and Cesium (Cs I). These were likely the immediate targets for the developer. Other alkali atoms (Li, Na, K, etc.) are not yet supported simply because their energy level data are not included. Extending to additional species would require adding their energy tables (ideally from NIST or literature) and any needed quantum defect info. This is a straightforward extension for future versions.
- **Plasma Conditions:** The model focuses on electron-impact broadening. Ion-induced quasi-static broadening is not explicitly calculated here. In many plasmas, ion Stark broadening (usually causing quasistatic broadening of line wings) can be important for hydrogen lines or highly charged emitters, but for neutral alkalis at moderate densities, electron collisions dominate the pressure broadening. If needed, ion broadening could be incorporated (e.g. using quasi-static approximation for ions) in future updates.
Density Scaling: As noted, the output is essentially normalized to per unit electron density. The current interface does not take electron density as an input. The user must scale the results to their desired $N_e$. A future improvement could be to allow N<sub>e</sub> as a parameter and have the code output the absolute width and shift for that density (saving the user a step and reducing potential confusion).
- **Accuracy and Validity Range:** Griem’s model is an approximation. Its accuracy tends to be within ~20% for many lines, but it may be less accurate for:
  - Very high principal quantum numbers (near ionization) where quantum defects and level mixing become complex.
  - Extremely high densities where the impact approximation starts to break down (collisions are no longer independent or the line may approach the quasistatic regime).
  - Very low electron velocities (or very low temperatures) where quantum effects (like Ramsauer-Townsend minima in cross-sections) are not captured by a purely classical model. The code does not currently warn the user about regimes of questionable validity. It assumes the user applies it within reasonable conditions (e.g. not for densities beyond the impact regime or temperatures where other broadening mechanisms dominate). A future version might include warnings or criterion checks (for example, comparing $\rho_{\min}$ to Debye length or ensuring impact parameter integrations converge).
- **Quantum Effects:** The current implementation is semi-classical. Future work could involve integrating quantum mechanical line shape calculations for comparison or including collisional profiles (not just Lorentzian width) if needed. For example, incorporating an option for detailed line profile computation (beyond just width & shift) would be valuable for spectroscopic diagnostics (though significantly more complex).
- **Perturbing States Selection:** The heuristic of choosing the nearest n_terms states by frequency difference might miss cases where a slightly further state with a much larger oscillator strength could contribute. Currently, the code orders by frequency (energy difference). Future improvement could involve ranking by actual expected impact on width (which could be a combination of frequency detuning and dipole matrix element). Additionally, when n_terms is more than 1, the code picks the top N states in terms of frequency closeness; it might be beneficial to pick symmetric numbers above and below if available (e.g., if you want 2 states, pick one above and one below). As of now, it does not guarantee an equal split. This selection strategy could be refined.
- **Performance:** For large velocity arrays or many perturbing states, the computation could slow down (though it should still be quite fast for typical use). There is room to optimize numerical integration or allow vectorized operations. Using SciPy’s integration routines or optimizing the root-solving for $\rho_{\min}$ (perhaps with analytical initial guesses) could speed up the calculations. So far, performance is sufficient for interactive use (e.g., integrating over 1000 velocity points is on the order of seconds).
- **Error Handling and Input Flexibility:** The code expects well-formatted state strings. A potential improvement is to make the input parsing more flexible or robust (for instance, accepting states like "5p3/2" lowercase, or principal quantum as integer and term letter separately). Currently, an exact match is needed (case-sensitive, no extra spaces). If an invalid state or element is provided, the error message may be a generic KeyError or ValueError. Improving user-facing error messages (e.g., “Element not supported” or “State not found in data”) would enhance usability.
- **Documentation and Examples:** As a future task, adding more examples (especially in a Jupyter notebook format with plots showing how line profiles might be constructed from the width and shift) would benefit users. Also, validating the code against published broadening parameters (for Rb and Cs lines) and including a comparison in the documentation would build confidence in the results.
- **GUI or CLI Interface:** For convenience, a small command-line interface or a GUI could be developed to allow non-programmers to input parameters and get results. This is beyond the scope of the current code but could be a nice addition for a wider user base.  


In summary, while the current version covers the essential functionality for Rb and Cs Stark broadening via Griem’s model, it is a foundation that can be extended to more elements, more sophisticated physics, and improved usability in future versions. Users are encouraged to cross-check important results with experimental data or other models whenever possible, and to treat results in extreme regimes with caution.  

## Dependencies
The Stark_Broadening-Griem package relies on several scientific Python libraries. These are automatically installed with pip, but for reference, the main dependencies are:
- **NumPy:** Used for numerical arrays and math operations throughout the calculations (e.g., vectorized computations of distributions, summations, etc.).
- **Pandas:** Used for handling tabular data (reading energy level Excel files into DataFrames, and manipulating state data). Pandas provides convenient DataFrame structures for the energy tables and for intermediate results.
-** SciPy:** Used for numerical routines like root-finding (scipy.optimize.fsolve in the $\rho_{\min}$ solver) and special functions (scipy.special for Bessel functions and the gamma function). SciPy is crucial for the accurate computation of the special functions A(z), B(z), etc., and for solving equations.
- **tabulate:** Used for pretty-printing tables in the console. The GriemResults.print() method uses tabulate to format the output in a readable table form. This is a lightweight dependency to make the CLI output more user-friendly.  

These dependencies are listed in the install_requires of setup.py and will be installed automatically. The code is compatible with Python 3.7+ and should work on any OS (Linux, Windows, macOS) as it is OS-independent (all calculations are in Python/NumPy).   
**Note on data files:** The package includes two data files (Excel spreadsheets) for energy levels of Rb and Cs. There is no additional database dependency; the data is local. Ensure that the installation places the `griem/data` folder in the correct location. The `load_energy_data` function will look for those files relative to the package directory. If you expand the repository or run from source, the files should be in `griem/data/`. If you experience a `FileNotFoundError` when loading data, it may indicate the data files are not in the expected path.  

## Acknowledgments

This project and its accompanying documentation were authored by Jordan Mindrup.

ChatGPT (OpenAI) was used as an assistant tool during the development of the code and the preparation of this README file. In particular, ChatGPT was used to help draft portions of the documentation, explain technical concepts, and assist in the formatting of the README. All content was reviewed, verified, and refined by the author.

The code logic, structure, and originality remain the author's own work, with AI used as a productivity and writing tool rather than a source of scientific content or computational methods.


## License
This project is released as open-source. In the absence of a specific license file in the repository, we default to a permissive license to encourage use and contribution. The code and data are (unless otherwise noted) distributed under the MIT **License**. This means you are free to use, modify, and distribute the code, provided that appropriate credit is given to the author.   

For details of the MIT License, one can refer to the standard text (in short: the software is provided "as is" without warranty, and the author is not liable for any issues arising from its use). If the repository is updated with a LICENSE file, that will take precedence and should be consulted.   

If you reuse significant portions of this code or incorporate it into your project, a mention of the original repository and author would be appreciated (see Citation below).

## Citation
If you use Stark_Broadening-Griem in academic research or publications, please consider citing it. There are two aspects you might want to cite:
1. **The software itself:** There is not yet a DOI or published paper specifically for this code (as of version 0.1.0), but you can cite it as a Zenodo reference if one is created in future, or simply in text as "J. Mindrup, Stark_Broadening-Griem code (Version 0.1.0), 2025, GitHub repository: https://github.com/Cassegrain10/Stark_Broadening-Griem".
2. **The underlying theory:** It is good practice to cite the original sources of the theory. The key references for Griem’s Stark broadening theory are:
3. **H. R. Griem, Physical Review 125, 177 (1962)** – which provides a detailed derivation of the impact broadening theory (originally for He I).
4. **H. R. Griem, Physical Review 128, 515 (1962)** – which applies the theory to neutral heavy elements (like Cs, Ar) and provides tables of widths and shifts.
5. **H. R. Griem, Spectral Line Broadening by Plasmas, Academic Press (1974)** – a comprehensive monograph covering Stark broadening in depth.
6. You may also cite relevant modern papers if you compare with or build upon their data. For example, any experimental papers for Rb or Cs Stark broadening measurements, or subsequent theoretical improvements, as appropriate for context.   

In summary, a citation in a publication might look like:
> "We computed the Stark broadened line widths using the Stark_Broadening-Griem code[^1], which implements Griem’s classical impact theory[^2]. Stark broadening parameters were taken from Griem’s formulation[^3]."

[^1]: https://github.com/Cassegrain10/Stark_Broadening-Griem
[^2]: https://journals.aps.org/pr/abstract/10.1103/PhysRev.128.515
[^3]: https://www.sciencedirect.com/science/article/pii/0022407381900893

Including the above references in your bibliography will credit both the code and the fundamental theory. If the author of this code (Jordan Mindrup) publishes a journal article or DOI for the software in the future, please update your citations accordingly. 
___

By following these guidelines and citing appropriately, you acknowledge the work behind the code and the theory. We hope this tool proves useful in your plasma spectroscopy and atomic physics research. Please report any issues or suggestions on the GitHub repository. Happy computing!
____
