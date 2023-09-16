# ==Solution==
from qiskit import QuantumCircuit

def constant_oracle(const_f: int, n_qubits: int) -> QuantumCircuit:
    """Create a quantum circuit that implements the constant oracle U_f for a given (single digit) binary that encodes the constant function f.
    The number of qubits, excluding a single ancilla qubit, is given by the argument n_qubits. """

    assert type(const_f) == int
    assert (const_f == 0) or (const_f ==1)

    assert type(n_qubits) == int
    assert n_qubits>0

    co = QuantumCircuit(n_qubits+1) # "+1" for the ancilla qubit

    # Apply X-gate on ancilla
    if const_f == 1:
        co.x(n_qubits)

    return co

# Example usage:
constant_oracle(1,3).draw()