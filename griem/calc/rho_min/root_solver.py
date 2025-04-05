"""
root_solver.py

Numerical root solver using the Brent method from SciPy.

Wraps `scipy.optimize.root_scalar` to provide a simplified interface
for solving scalar equations over a bracketing interval. Automatically
raises a clear error if the solver fails to converge.
"""


# Import modules
from scipy.optimize import root_scalar

def solve(
        func: callable, 
        domain_bracket: list, 
        *args, 
        method: str = 'brentq'):
    """
    Solve a scalar nonlinear equation using a root-finding method (default: Brent's method).

    This function wraps `scipy.optimize.root_scalar`, allowing additional arguments to
    be passed to the function being solved. If the solver fails to converge or encounters
    an error, a ValueError is raised with context.

    Args:
        func (callable): Function of one variable to solve. Additional arguments are passed via *args.
        domain_bracket (list or tuple): Two-element bracket [a, b] where the root is expected.
        *args: Additional arguments passed to `func`.
        method (str, optional): Root-finding method used by `root_scalar`. Default is 'brentq'.

    Returns:
        float: The root of the function within the provided bracket.

    Raises:
        ValueError: If the solver fails to converge or another error occurs.
    """
    def f(x):
        return func(x, *args)

    try:
        sol = root_scalar(f, bracket=domain_bracket, method=method)
        if not sol.converged:
            raise ValueError(f"Solution did not converge withing bracket {domain_bracket}")
        return sol.root
    except Exception as e:
        raise ValueError(f"Error in root finding: {e}")
    
