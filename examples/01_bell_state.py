from quantum_leap import QuantumCircuit, plot_histogram

# 1. Create a quantum circuit with 2 qubits
qc = QuantumCircuit(2)

# 2. Apply gates to create a Bell state (|Φ+>)
# Apply Hadamard gate to the first qubit (q0)
qc.h(0)
# Apply CNOT gate with q0 as control and q1 as target
qc.cnot(0, 1)

# 3. Simulate the circuit
# Run the simulation 1024 times
results = qc.run(shots=1024)

# 4. Print and plot the results
print("Bell State Simulation Results:")
print(results)
plot_histogram(results, title="Bell State Entanglement")
# Expected outcome: Roughly 50% '00' and 50% '11'
