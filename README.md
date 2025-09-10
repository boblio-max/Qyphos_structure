# QuantumLeap: A Python Quantum Computer Emulator

QuantumLeap is a lightweight, educational quantum computing emulator written in Python. It uses NumPy for efficient state vector simulation and provides a clean, object-oriented API for building and running quantum circuits.

## Features

- **Qubit Simulation**: Simulates up to 15 qubits on a standard laptop.
- **State Vector Representation**: Represents multi-qubit systems using complex state vectors.
- **Comprehensive Gate Library**: Implements all standard gates: X, Y, Z, H, S, T, CNOT, CZ, SWAP, and parameterized rotations RX, RY, RZ.
- **User-Friendly API**: An intuitive `QuantumCircuit` class for easy circuit construction.
- **Probabilistic Measurement**: Simulates realistic measurement outcomes with statistical results.
- **Visualization**: Includes built-in tools to plot measurement histograms with Matplotlib.

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/quantum-leap-emulator.git](https://github.com/your-username/quantum-leap-emulator.git)
    cd quantum-leap-emulator
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Quick Start

Create and simulate a Bell state in just a few lines of code.

```python
from quantum_leap import QuantumCircuit, plot_histogram

# 1. Create a quantum circuit with 2 qubits
qc = QuantumCircuit(2)

# 2. Apply gates to create an entangled Bell state
qc.h(0)
qc.cnot(0, 1)

# 3. Simulate the circuit with 1024 measurements ("shots")
results = qc.run(shots=1024)

# 4. Print and plot the results
print(results)
plot_histogram(results, title="Bell State Entanglement")
