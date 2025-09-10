"""
Example: Simulating T1 Relaxation Noise

This script demonstrates how to use the density matrix simulator to model
a common type of quantum error: T1 relaxation, where a qubit in state |1>
decays to state |0> over time.
"""
from quantum_leap import QuantumCircuit
from quantum_leap.noise import AmplitudeDamping
from quantum_leap.visualizer import plot_histogram, plot_density_matrix
import numpy as np

# --- Simulation Parameters ---
NUM_QUBITS = 1
# Probability of decay after one "time step"
DECAY_PROBABILITY = 0.2 
SHOTS = 4096

# --- 1. Ideal Circuit (No Noise) ---
print("--- Running Ideal Simulation (No Noise) ---")
# Use the default 'statevector' mode for the ideal case
ideal_qc = QuantumCircuit(NUM_QUBITS)
ideal_qc.x(0) # Prepare the qubit in state |1>
ideal_qc.draw()
ideal_results = ideal_qc.run(shots=SHOTS)
plot_histogram(ideal_results, "Ideal Circuit: Qubit prepared in |1>")
# Expected: 100% of measurements are '1'

# --- 2. Noisy Circuit (With T1 Decay) ---
print("\n--- Running Noisy Simulation (With T1 Decay) ---")
# IMPORTANT: Switch to 'density_matrix' mode to enable noise
noisy_qc = QuantumCircuit(NUM_QUBITS, mode='density_matrix')

# Define the noise model
t1_decay = AmplitudeDamping(decay_probability=DECAY_PROBABILITY)

# Build the circuit
noisy_qc.x(0) # Prepare the qubit in state |1>
noisy_qc.barrier()
# Add the noise channel to simulate the qubit idling and decaying
noisy_qc.add_noise(t1_decay, qubits=[0]) 

# Draw the noisy circuit
noisy_qc.draw()

# Run the simulation
noisy_results = noisy_qc.run(shots=SHOTS)
plot_histogram(noisy_results, f"Noisy Circuit: T1 Decay (p={DECAY_PROBABILITY})")
# Expected: Some counts for '0' will appear due to decay from |1> to |0>

# Visualize the final density matrix
final_dm = noisy_qc.get_state()
plot_density_matrix(final_dm, "Final Density Matrix After T1 Decay")
