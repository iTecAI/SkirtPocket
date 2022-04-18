"""
Simpson's method solver (generalized) [python 3.10]

Dax Harris 2022
"""

import math
import numpy as np

"""
Utility function for applying linspace to arbitrary functions
"""
def fn_synth(arr: np.ndarray, fn):
    out = []
    for i in arr.tolist():
        out.append(fn(i))
    return out

"""
Implementation of simpson's method (1/3)
"""
def simpson(
    fn, # A function that represents f(x)
    a: float, # Interval lower bound
    b: float, # Interval upper bound
    n: int # Number of subintervals
) -> float:
    h = (b - a) / (n - 1)
    if ((n-1) % 2 == 1):
        raise ValueError("N must be odd")
    x = np.linspace(a, b, n) # Generate linearly spaced points
    f = fn_synth(x, fn) # Calculate fn(x) for points in linspace

    # Calculate result
    result = (h/3) * (f[0] + 2*sum(f[:n-2:2]) + 4*sum(f[1:n-1:2]) + f[n-1])
    return result

# = = = TESTS = = =

def f(x):
    return x * math.sin(x)

if __name__ == "__main__":
    print(simpson(f, 1, 4, 1001)) # Test on f(x) = xsin(x) over 1000 subintervals (~0.002 error)

__all__ = ["simpson"] # Only export the main function to other code

