"""
Arbitrary function resolver (changes the input of a function until the output is within a threshold of a desired value)

Dax Harris 2022
"""

import math
__all__ = ["resolve"]

def resolve(
    fn, # Function to check
    target: float, # Target output
    lower: float, # Lower bound of values to check
    upper: float, # Upper bound of values to check
    allowed_error: float, # Allowed error
    samples: int = 1000, # Number of random samples per iteration
    keep: int = 10, # Number of samples to keep
    shrink: float = 5 # Multiple to shrink bounds by for each recursion
) -> list[float]:

    # Generate list of results
    results = []
    for s in range(samples):
        inp = lower + ((upper - lower) / samples) * s
        try:
            res = fn(inp)
            results.append([res, inp, abs(res-target)]) # [result, input, error]
        except ZeroDivisionError:
            pass
    
    # Get closest <keep> samples
    results.sort(key=lambda x: x[2])
    results = results[:keep]

    # Check each close result, recurse if not close enough
    recursive_output = []
    for r in results:
        if r[2] <= allowed_error:
            return r
        
        # Shrink bounds
        bound_width = (upper-lower) / shrink

        # Recursively test with new bounds
        try:
            res = resolve(
                fn, 
                target, 
                r[1]-bound_width, 
                r[1]+bound_width, 
                allowed_error, 
                samples=samples, 
                keep=keep, 
                shrink=shrink
            )
            recursive_output.append(res)
            if res[2] <= allowed_error:
                break
        except RecursionError:
            recursive_output.append(r[:])
    
    # Sort for best result
    recursive_output.sort(key=lambda x: x[2])
    return recursive_output[0]

# === TEST ===

import math

def f(x):
    return (3*(x**3))*(math.sin(x))*(math.cos(x)/x)

if __name__ == "__main__":
    print(resolve(f, 5, 0, 8*math.pi, 0.0001))

