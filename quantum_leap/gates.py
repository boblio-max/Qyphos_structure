"""
Defines quantum gate matrices and operators.
All matrices are created using the configured backend (NumPy or CuPy).
"""
from . import backends as be

# --- Gate Definitions (now backend-agnostic) ---
I = be.array([[1, 0], [0, 1]], dtype=be.complex_type)
X = be.array([[0, 1], [1, 0]], dtype=be.complex_type)
Y = be.array([[0, -1j], [1j, 0]], dtype=be.complex_type)
Z = be.array([[1, 0], [0, -1]], dtype=be.complex_type)
H = (1 / be.sqrt(be.array([2.0]))) * be.array([[1, 1], [1, -1]], dtype=be.complex_type)
S = be.array([[1, 0], [0, 1j]], dtype=be.complex_type)
T = be.array([[1, 0], [0, be.exp(1j * be.array([be.pi / 4]))]], dtype=be.complex_type)

def RX(theta: float):
    c = be.cos(theta / 2)
    s = be.sin(theta / 2)
    return be.array([[c, -1j * s], [-1j * s, c]], dtype=be.complex_type)

def RY(theta: float):
    c = be.cos(theta / 2)
    s = be.sin(theta / 2)
    return be.array([[c, -s], [s, c]], dtype=be.complex_type)

def RZ(phi: float):
    p = be.exp(-1j * phi / 2)
    return be.array([[p, 0], [0, p.conj()]], dtype=be.complex_type)

# --- Operator Construction ---
def _get_operator_internal(num_qubits, gate_list):
    """Internal helper to construct an operator from a list of gates via tensor product."""
    op = be.array([1], dtype=be.complex_type)
    for i in range(num_qubits):
        op = be.kron(op, gate_list[i])
    return op

def get_operator(num_qubits: int, gate: be.array, target_qubit: int):
    """Constructs the full system operator for a single-qubit gate."""
    gate_list = [I] * num_qubits
    gate_list[target_qubit] = gate
    return _get_operator_internal(num_qubits, gate_list)

def get_controlled_operator(num_qubits, gate, control, target):
    """Constructs the full system operator for a two-qubit controlled gate."""
    P0 = be.array([[1, 0], [0, 0]], dtype=be.complex_type)
    P1 = be.array([[0, 0], [0, 1]], dtype=be.complex_type)

    term0_list = [I] * num_qubits
    term0_list[control] = P0
    
    term1_list = [I] * num_qubits
    term1_list[control] = P1
    term1_list[target] = gate

    return _get_operator_internal(num_qubits, term0_list) + \
           _get_operator_internal(num_qubits, term1_list)
