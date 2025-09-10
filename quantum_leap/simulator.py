"""
The core simulation engine. It takes a list of circuit operations
and applies them to a quantum state (state vector or density matrix).
"""
import numpy as np
from typing import List, Tuple, Dict
from tqdm import tqdm

from . import backends as be
from . import gates

def _apply_gate_statevector(state_vector: be.array, op: be.array) -> be.array:
    return be.dot(op, state_vector)

def _apply_gate_density_matrix(density_matrix: be.array, op: be.array) -> be.array:
    op_dagger = be.conj(op).T
    return be.dot(op, be.dot(density_matrix, op_dagger))

def _apply_noise_channel(density_matrix: be.array, kraus_ops: List[be.array], target_qubit: int, num_qubits: int) -> be.array:
    new_density_matrix = be.zeros(density_matrix.shape, dtype=be.complex_type)
    for K in kraus_ops:
        full_K = gates.get_operator(num_qubits, K, target_qubit)
        full_K_dagger = be.conj(full_K).T
        term = be.dot(full_K, be.dot(density_matrix, full_K_dagger))
        new_density_matrix += term
    return new_density_matrix

class Simulator:
    def __init__(self, num_qubits: int, mode: str = 'statevector'):
        self.num_qubits = num_qubits
        self.mode = mode
        self.state = self._initialize_state()

    def _initialize_state(self):
        dim = 2**self.num_qubits
        if self.mode == 'statevector':
            state = be.zeros(dim, dtype=be.complex_type)
            state[0] = 1.0
            return state
        elif self.mode == 'density_matrix':
            dm = be.zeros((dim, dim), dtype=be.complex_type)
            dm[0, 0] = 1.0
            return dm
        else:
            raise ValueError("Unsupported simulation mode. Choose 'statevector' or 'density_matrix'.")

    def run(self, operations: List[Tuple]):
        print(f"🚀 Simulating circuit with {self.num_qubits} qubits in '{self.mode}' mode...")
        for op_name, op_params in tqdm(operations, desc="Applying gates"):
            if op_name == 'barrier':
                continue # Barriers are for visualization only

            if op_name in ['h', 'x', 'y', 'z', 's', 't', 'rx', 'ry', 'rz']:
                gate_func = getattr(gates, op_name.upper() if len(op_name) == 1 else op_name)
                gate = gate_func(op_params[0]) if isinstance(op_params, tuple) else gate_func
                op = gates.get_operator(self.num_qubits, gate, op_params if isinstance(op_params, int) else op_params[1])
            
            elif op_name in ['cnot', 'cz']:
                gate = gates.X if op_name == 'cnot' else gates.Z
                op = gates.get_controlled_operator(self.num_qubits, gate, op_params[0], op_params[1])
            
            elif op_name == 'noise':
                if self.mode != 'density_matrix':
                    print("⚠️ Warning: Noise can only be simulated in 'density_matrix' mode. Skipping noise operation.")
                    continue
                noise_channel, target_qubit = op_params
                kraus_ops = noise_channel.get_kraus_operators()
                self.state = _apply_noise_channel(self.state, kraus_ops, target_qubit, self.num_qubits)
                continue # Skip the unified gate application below

            else:
                raise ValueError(f"Unknown operation: {op_name}")

            # Apply the constructed gate operator
            if self.mode == 'statevector':
                self.state = _apply_gate_statevector(self.state, op)
            else:
                self.state = _apply_gate_density_matrix(self.state, op)
        print("✅ Simulation complete.")
        return self.state

    def measure(self, shots: int) -> Dict[str, int]:
        if self.mode == 'statevector':
            probabilities = be.abs(self.state)**2
        else: # density_matrix
            probabilities = be.diag(self.state).real

        probabilities_np = be.to_numpy(probabilities)
        probabilities_np /= np.sum(probabilities_np) # Normalize

        outcomes = np.random.choice(len(probabilities_np), size=shots, p=probabilities_np)
        
        counts = {}
        for result in outcomes:
            bitstring = format(result, f'0{self.num_qubits}b')
            counts[bitstring] = counts.get(bitstring, 0) + 1
        return counts
