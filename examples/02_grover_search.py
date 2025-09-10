from quantum_leap import QuantumCircuit, plot_histogram
import numpy as np

# --- Define the Oracle for the state |11> ---
# The oracle flips the phase of the marked item. For |11>, this is a CZ gate.
def oracle(qc):
    qc.cz(0, 1)

# --- Define the Diffuser (Inversion about the mean) ---
def diffuser(qc):
    qc.h(0)
    qc.h(1)
    qc.x(0)
    qc.x(1)
    qc.cz(0, 1)
    qc.x(0)
    qc.x(1)
    qc.h(0)
    qc.h(1)

# --- Build the Circuit ---
# For N=4 (2 qubits), we only need 1 iteration.
NUM_QUBITS = 2
qc = QuantumCircuit(NUM_QUBITS)

# 1. Initialize to uniform superposition
qc.h(0)
qc.h(1)

# 2. Apply Grover's algorithm (Oracle + Diffuser)
print("Applying Oracle and Diffuser...")
oracle(qc)
diffuser(qc)

# 3. Simulate the circuit
results = qc.run(shots=1024)

# 4. Print and plot results
print("\nGrover's Search Results:")
print(results)
plot_histogram(results, title="Grover's Search for |11>")
# Expected outcome: High probability of measuring '11'
