"""
QuantumLeap Backend Manager.

This module automatically selects and configures the numerical backend for the simulation.
It prioritizes CuPy for GPU acceleration and falls back to NumPy for CPU execution.
All other modules should import the `backend` object from here to remain hardware-agnostic.
"""
import os

# --- Backend Selection ---
BACKEND_CHOICE = os.environ.get('QL_BACKEND', 'auto').lower()
_backend_name = "numpy"

if BACKEND_CHOICE in ('cupy', 'auto'):
    try:
        import cupy as backend
        _backend_name = "cupy (GPU)"
    except ImportError:
        if BACKEND_CHOICE == 'cupy':
            raise ImportError("CuPy backend was requested, but CuPy is not installed.")
        import numpy as backend
        _backend_name = "numpy (CPU)"
else:
    import numpy as backend
    _backend_name = "numpy (CPU)"

print(f"✅ QyphosStructure: Initialized with {_backend_name} backend.")

# Expose the chosen backend's functions
# This allows other modules to call `backend.array`, `backend.kron`, etc.
# without knowing whether they are using NumPy or CuPy.
array = backend.array
kron = backend.kron
eye = backend.eye
dot = backend.dot
zeros = backend.zeros
sqrt = backend.sqrt
exp = backend.exp
cos = backend.cos
sin = backend.sin
abs = backend.abs
diag = backend.diag
einsum = backend.einsum
asarray = backend.asarray
conj = backend.conj

# --- Data Types ---
complex_type = backend.complex128 if _backend_name.startswith("numpy") else backend.complex64
float_type = backend.float64 if _backend_name.startswith("numpy") else backend.float32

def to_numpy(data):
    """Converts data from a backend array (like CuPy) to a NumPy array."""
    if 'cupy' in str(type(data)):
        return data.get()
    return data
