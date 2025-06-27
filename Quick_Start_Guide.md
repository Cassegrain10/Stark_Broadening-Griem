## Quick Start Guide
The rest of this document will be helpful if you want to dig deep into the inner workings if thr code. However, the best way to learn is to just do it. This Quick Start Guide should get you up and running in no time!  

**Also, you can find an example in this [Google Collab Notebook](https://colab.research.google.com/drive/1Eg_v6B0cknq5qMLnNXKILML9KmvS01r5).**

### Installing the Library
The first step is of if course, install the library. This step depends of course on what encironment you are using Griem in: cloud-based in *Google Collab*, or locally in Python on your device. 

#### Option 1: Cloud-Based on Google Collab
At the very beginning of your notebook, you will include this,
```python
# Importing `Stark_Broadening-Griem` library into environment
!pip install git+https://github.com/Cassegrain10/Stark_Broadening-Griem.git

#===============
# Import Libraries
# ...
#===============
```
And it's that easy! For that reason I _highly_ recomend using [Google Collab](https://colab.research.google.com/). 


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

### Understanding the Library
Before we dive into useage examples, understanding the inluts into thr API is crucial. 
### Using the Library
Now we will go over several examples on how to use the library. The onlh orr of the library that the user will interface with for thr calculations is the Griem class. The Griem class is
a complete API that calls the main calculation engine. Below is the docstring-style structure of the Griem API:

```python
class Griem:
    """
    The main API for the griem calculation.

    The `Griem` class provides a simple API for the calculation of Stark widths and shifts to 
    electron collisionally broadened transitions in Alkalis. The user specifies the alkali, the 
    lower state, the upper state, the velocity, EVDF, and the number of terms to include in the 
    calculation summation (i.e. the number of perturbing states to include in the calculation). 
    For a detailed derivation of the theory, see Physical Review, 125 177, and for experimental
    benchmarks of the theory see Physical Review, 128 515.

    Attributes:
        element (str): The alkali element symbol (e.g. 'Rb').
        lower_state (str): Lower state of the transition (e.g. '4D3/2').
        upper_state (str): Upper state(s) of the transition (e.g. '12F5/2' or 'F5/2').
        velocity (float, np.ndarray): Velocity of the electrons - can be a single value (v_bar),
                                      or it can be an array of velocities used with an EVDF.
        EVDF (float, np.ndarray): Electron velocity distribution function (e.g. Maxwell-Boltzmann).
        n_terms (int): The number of perturbing states to include in the calculation.

        energy_data (Table): The energy data used for the calculation.
        processed_data (AliasDict): Contains all the dataframes of calculation data.
        results (GriemResults): Contains the widths, shifts, and a table of the widths and shifts.

    Methods:
        calculate(): Run the Griem calculation for the provided input.

    Example:
        >>> griem = Griem("Rb", "4D3/2", "12F5/2", 4e5, n_terms=4)
        >>> griem.calculate()
        >>> griem.results.print()

    """
    def __init__(
            self, 
            element: str, 
            lower_state: str, 
            upper_state: str, 
            velocity: Union[float, np.ndarray], 
            EVDF: Union[float, np.ndarray] = 1.0
        ):
        """Initialize a Griem object for line calculations.

        Args:
            element (str): The alkali element symbol (e.g. 'Rb').
            lower_state (str): Lower state of the transition (e.g. '4D3/2').
            upper_state (str): Upper state(s) of the transition (e.g. '12F5/2' or 'F5/2').
            velocity (float, np.ndarray): Velocity of the electrons - can be a single value (v_bar),
                                          or it can be an array of velocities used with an EVDF.
            EVDF (float, np.ndarray, optional): Electron velocity distribution function (e.g. 
                                                Maxwell-Boltzmann). Defaults to 1.0.
            n_terms (int, optional): The number of perturbing states to include in the calculation. 
                                     Defaults to 1.
        """
```
Following is a brief overview of the parameters, attributes, and methods of the `Griem` class. `Griem` is a class, so it has attributes - sets of **variables that belong to the class**; and methods - sets of **functions that belong to the class**. The parameters are what the user inputs to the class when it is instantiated (kind of like a function). Attributes can be derived from the input parameters, but they don't have to be.  
- **Parameters**: what the user inputs into the class when the class is instantiated. 
- **Attributes**: set of variables that belong to the class. To access an attribute, `my_attr`, in a class, `my_class` -> `my_class.my_attr`.
- **Methods**: set of functions that belong to the class. To call the method, `my_method`, in a class, `myclass` -> `my_class.my_method()`.

If you are not familiar with classes in Python, and want to learn more, be sure to check out the helpful article, [Object-Oriented Programming (OOP) in Python](https://realpython.com/python3-object-oriented-programming/), or the offical [Python documentation](https://docs.python.org/3/tutorial/classes.html) on classes.
Below is a table summarizing the parameters of the `Griem` class:
| Parameter     | Type             | Description                             | Required? |
| ------------- | ---------------- | --------------------------------------- | --------- |
| `element`     | `str`            | Alkali element symbol (e.g., `'Rb'`)    | Yes       |
| `lower_state` | `str`            | Lower state of the transition           | Yes       |
| `upper_state` | `str`            | Upper state of the transition           | Yes       |
| `velocity`    | `float or array` | Electron velocity or distribution       | Yes       |
| `EVDF`        | `array`          | Electron velocity distribution function | No        |

Below is a table that summarizes the attributes of the `Griem` class:
| Attribute        | Type                     | Description                                                   |
| ---------------- | ------------------------ | ------------------------------------------------------------- |
| `element`        | `str`                    | Alkali element symbol (copied from constructor input).        |
| `lower_state`    | `str`                    | Lower state of the transition.                                |
| `upper_state`    | `str`                    | Upper state(s) of the transition.                             |
| `velocity`       | `float` or `np.ndarray`  | Electron velocity or distribution.                            |
| `EVDF`           | `float` or `np.ndarray`  | Electron velocity distribution function.                      |
| `n_terms`        | `int`                    | Number of perturbing states used in the summation.            |
| `energy_data`    | `Table`                  | Energy level data used in the calculation.                    |
| `processed_data` | `AliasDict`              | Intermediate and processed data as named dataframes.          |
| `results`        | `GriemResults` (`class`) | Object containing Stark widths, shifts, and tabulated output. |

And a summary of the Griem class' only method:
| Method        | Description                                                                         |
| ------------- | ----------------------------------------------------------------------------------- |
| `calculate()` | Performs the Griem calculation based on initialized state and velocity information. |

And the parameters of that method, both being **optional**:
| Parameter              | Type   | Default | Description                                                       |
| ---------------------- | ------ |-------- | ----------------------------------------------------------------- |
| `num_terms`            | `int`  | `1`     | Number of perturbing states to include in the summation.          |
| `want_interact_states` | `bool` | `False` | Whether to include interacting states in the final results table. |



Below is a **helpful illustration**:
```python
# Instantiate the Griem class
stark = Griem(element='Rb',
              lower_state = '4D3/2',
              upper_state = '15F5/2',
              velocity = 4.5e5)
```
This _instantiates_ the class - creates an _instance_ of the `Griem`. The parameters are the values assigned in the instantiation above. When the `Griem` class is instantiated, some of the attributes are created by default - for example, the `element`, `lower_state`, `upper_state`, `velocity`, and `EVDF` attributes are populated immediately upon instantiation [^1]
[^1]: Note here that while all of the attributes are the same as the parameters, this is not the case for all classes. This is done here so that that the user can change the `Griem` attributes later.
```python
# Perform the broadening calculation
stark.calculate(num_terms=4)
```
Here we use the method, `calculate()` - it perfroms an action (functon) within the class - in our case it calculates the broadening width and shift. Yep, that's right - in one line the complete Griem calculation is performed! Here the parameter `num_terms` (the number of perterbing states included in the calculation) is set to `num_terms=4`, and the parameter `want_interact_states` (whether or not to include in the printed results the term symbols of the perterbing states included in the calculation) was left at its default of `want_interact_states=False`. The broadening calculation has been performed - now all that is left is to display and save the results! This is where the attribute `results` of the `Griem` class comes in. 

The `results` attribute is itself a class - the `GriemResults` class:

```
class GriemResults():
    """
    Container for Stark width and shift results from a Griem calculation.

    This class extracts and organizes the real and imaginary components of the 
    complex output from a Griem calculation, corresponding to the Stark broadened 
    linewidth (width) and shift, respectively. It provides methods for displaying 
    and exporting the results in a tabular format.

    Attributes:
        states (list or np.ndarray): Upper electronic states corresponding to each result.
        width (float or np.ndarray): Stark broadened linewidths (real part of input).
        shift (float or np.ndarray): Stark line shifts (imaginary part of input).
        ratio (float or np.ndarray): Shift-to-width ratio (d/w) for each state.
        table (Table): A formatted table object for printing and saving results.

    Methods:
        print():
            Prints the formatted results table to the terminal.
        
        save(filename="griem.csv"):
            Saves the results table to a CSV or Excel (.xlsx) file.

    Args:
    ....
    ......
    ........
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
```
For this class we don't have any public parameters, as this class gets immediately instantiated upon calling the `calculate()` method of the `Griem` class, the input parameters being automatically input to `GriemResults`. Below is a table summarizing the attributes:
| Attribute | Type                    | Description                                                                       |
| --------- | ----------------------- | --------------------------------------------------------------------------------- |
| `states`  | `list` or `np.ndarray`  | Upper electronic states for which results were calculated.                        |
| `width`   | `float` or `np.ndarray` | Stark broadened linewidths (real part of `width_shift`).                          |
| `shift`   | `float` or `np.ndarray` | Stark line shifts (imaginary part of `width_shift`).                              |
| `ratio`   | `float` or `np.ndarray` | Ratio of shift to width (`shift / width`).                                        |
| `table`   | `Table`                 | Tabulated results (states, width, shift, d/w, and optionally interaction states). |

These are the attributes that the user will be directly calling to get the results - `states`, `width`, `shift` are the common ones that the user will utilize. Below is a table summarizing the methods:
| Method    | Description                                                              |
| --------- | ------------------------------------------------------------------------ |
| `print()` | Prints the formatted results table to the terminal.                      |
| `save()`  | Saves the results table to a CSV or Excel file (`griem.csv` by default). |

Both of these methods are extremely useful. In fact, let's pick up where we left off with our above illustration. We left off with `stark.calculate(num_terms=4)`. Now we want to print and save the results:
```python
# Printing the broadening results for the 4D3/2 -> 15F5/2 transition
stark.results.print()
```
```
=======================Griem Results=======================
| Upper state   |       Width |        Shift |       d/w |
|---------------|-------------|--------------|-----------|
| 15F5/2        | 6.89965e-09 | -2.49753e-09 | -0.361979 |
```
```python
# Saving the results
stark.results.save("broadening_results.csv")
```
The filetype for `GriemResults.save()` can be '.csv' or '.xlsx'.  

We can also include the interacting states if we wish:
```python
# Perform the broadening calculation
stark.calculate(num_terms=4, want_interact_states=True)

# Printing the broadening results for the 4D3/2 -> 15F5/2 transition
stark.results.print()

# Saving the results
stark.results.save("broadening_results.csv")
```
```
=========================================Griem Results=========================================
| Upper state   |       Width |        Shift |       d/w | Interaction states                 |
|---------------|-------------|--------------|-----------|------------------------------------|
| 15F5/2        | 6.89965e-09 | -2.49753e-09 | -0.361979 | -15G7/2, +16D5/2, -17D5/2, -16G7/2 |
```
Notice how we didn't have to reinstantiate the `Griem` class - we already did that. We just re-called the method `calculate()` and performed the calculation again. Additionally you can even change the parameters; for example you could now add an EVDF, and integrate over the entire velocity space:
```python
# Define Maxwell-Boltzmann distribution
def maxwell_boltzmann(velocity, temperature):
    ...
    ...
    return eevdf

# Define velocity space
import numpy as np
velocity = np.linspace(0.5, 5e6, 1000)

# Modify `stark` class
stark.velocity = velocity
stark.EVDF = maxwell_boltzmann(velocity=velocity, temperature=1000)

# Perform the broadening calculation
stark.calculate(num_terms=10)

# Printing the broadening results for the 4D3/2 -> 15F5/2 transition
stark.results.print()

# Saving the results
stark.results.save("broadening_results.xlsx")
```
```
=======================Griem Results=======================
| Upper state   |       Width |        Shift |       d/w |
|---------------|-------------|--------------|-----------|
| 15F5/2        | 9.35941e-09 | -6.75523e-09 | -0.721758 |
```
Hopefully, that illustration clearly shows the features of the `Griem` API.
