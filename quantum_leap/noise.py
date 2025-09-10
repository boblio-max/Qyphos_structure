"""
Defines common quantum noise channels using the Kraus operator formalism.
"""
from . import backends as be

class NoiseChannel:
    """Base class for noise channels."""
    def __init__(self, probability: float):
        if not (0 <= probability <= 1):
            raise ValueError("Probability must be between 0 and 1.")
        self.p = probability
        self.kraus_operators = []

    def get_kraus_operators(self) -> list:
        raise NotImplementedError

class DepolarizingChannel(NoiseChannel):
    """
    Applies a depolarizing error (X, Y, or Z gate) with a given probability.
    This models a general loss of information.
    """
    def get_kraus_operators(self) -> list:
        p = self.p
        K0 = be.sqrt(1 - p) * be.eye(2, dtype=be.complex_type)
        K1 = be.sqrt(p / 3) * be.array([[0, 1], [1, 0]], dtype=be.complex_type)  # X
        K2 = be.sqrt(p / 3) * be.array([[0, -1j], [1j, 0]], dtype=be.complex_type) # Y
        K3 = be.sqrt(p / 3) * be.array([[1, 0], [0, -1]], dtype=be.complex_type)  # Z
        return [K0, K1, K2, K3]

class AmplitudeDamping(NoiseChannel):
    """
    Models energy dissipation (T1 decay), the process of a qubit relaxing from |1> to |0>.
    """
    def __init__(self, decay_probability: float):
        super().__init__(decay_probability)

    def get_kraus_operators(self) -> list:
        gamma = self.p
        K0 = be.array([[1, 0], [0, be.sqrt(1 - gamma)]], dtype=be.complex_type)
        K1 = be.array([[0, be.sqrt(gamma)], [0, 0]], dtype=be.complex_type)
        return [K0, K1]

class PhaseDamping(NoiseChannel):
    """
    Models dephasing (T2 decay), the loss of phase information without energy loss.
    """
    def __init__(self, dephasing_probability: float):
        super().__init__(dephasing_probability)

    def get_kraus_operators(self) -> list:
        lambda_val = self.p
        K0 = be.array([[1, 0], [0, be.sqrt(1 - lambda_val)]], dtype=be.complex_type)
        K1 = be.array([[0, 0], [0, be.sqrt(lambda_val)]], dtype=be.complex_type)
        return [K0, K1]
