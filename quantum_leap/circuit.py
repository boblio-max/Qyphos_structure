from typing import Dict, List
from .simulator import Simulator
from .noise import NoiseChannel

class QuantumCircuit:
    def __init__(self, num_qubits: int, mode: str = 'statevector'):
        if num_qubits < 1:
            raise ValueError("Number of qubits must be at least 1.")
        self.num_qubits = num_qubits
        self.mode = mode
        self.operations = []
        self._final_state = None

    def _add_op(self, name: str, params):
        self.operations.append((name, params))
        self._final_state = None # Invalidate cache

    # --- Gate Methods (now add to operation list) ---
    def h(self, qubit: int): self._add_op('h', qubit)
    def x(self, qubit: int): self._add_op('x', qubit)
    def y(self, qubit: int): self._add_op('y', qubit)
    def z(self, qubit: int): self._add_op('z', qubit)
    def s(self, qubit: int): self._add_op('s', qubit)
    def t(self, qubit: int): self._add_op('t', qubit)
    def rx(self, theta: float, qubit: int): self._add_op('rx', (theta, qubit))
    def ry(self, theta: float, qubit: int): self._add_op('ry', (theta, qubit))
    def rz(self, phi: float, qubit: int): self._add_op('rz', (phi, qubit))
    def cnot(self, control: int, target: int): self._add_op('cnot', (control, target))
    def cz(self, control: int, target: int): self._add_op('cz', (control, target))
    def swap(self, qubit1: int, qubit2: int):
        self.cnot(qubit1, qubit2); self.cnot(qubit2, qubit1); self.cnot(qubit1, qubit2)

    # --- Advanced Operations ---
    def barrier(self):
        """Adds a visual barrier in the circuit diagram."""
        self._add_op('barrier', None)
        
    def add_noise(self, noise_channel: NoiseChannel, qubits: List[int]):
        """Adds a noise channel to specific qubits."""
        if self.mode != 'density_matrix':
            print("⚠️ Warning: Noise models require 'density_matrix' mode. This operation will be ignored.")
        for q in qubits:
            self._add_op('noise', (noise_channel, q))

    # --- Execution ---
    def _simulate(self):
        if self._final_state is None:
            sim = Simulator(self.num_qubits, self.mode)
            self._final_state = sim.run(self.operations)
        return self._final_state
        
    def get_state(self):
        return self._simulate()

    def run(self, shots: int = 1024) -> Dict[str, int]:
        self._simulate() # ensure state is calculated
        sim = Simulator(self.num_qubits, self.mode)
        sim.state = self._final_state
        return sim.measure(shots)

    # --- Visualization ---
    def draw(self):
        """Renders a text-based diagram of the circuit."""
        lanes = [f'q{i}: |0>──' for i in range(self.num_qubits)]
        
        for op_name, op_params in self.operations:
            if op_name == 'barrier':
                for i in range(self.num_qubits): lanes[i] += '──╫──'
                continue

            gate_width = len(op_name) + 2
            
            if op_name in ['h', 'x', 'y', 'z', 's', 't']:
                q = op_params
                lanes[q] += f'─[{op_name.upper()}]─'
                for i in range(self.num_qubits):
                    if i != q: lanes[i] += '─' * (gate_width + 2)

            elif op_name in ['rx', 'ry', 'rz']:
                q = op_params[1]
                gate_str = f"{op_name.upper()}"
                lanes[q] += f'─[{gate_str}]─'
                for i in range(self.num_qubits):
                    if i != q: lanes[i] += '─' * (len(gate_str) + 4)
            
            elif op_name in ['cnot', 'cz']:
                control, target = op_params
                ctrl_char = '●'
                target_char = 'X' if op_name == 'cnot' else 'Z'
                
                min_q, max_q = min(control, target), max(control, target)

                lanes[control] += f'──{ctrl_char}──'
                lanes[target] += f'─[{target_char}]─'
                for i in range(self.num_qubits):
                    if i not in [control, target]:
                        lanes[i] += '───' if not (min_q < i < max_q) else '──|──'
                
                for i in range(min_q + 1, max_q):
                    lanes[i] = lanes[i][:-3] + '──|──'
        
        print("\nCircuit Diagram:")
        for lane in lanes:
            print(lane)
        print()
