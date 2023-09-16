# ==Solution==
from qiskit import QuantumCircuit

def balanced_oracle(bitstring: str) -> QuantumCircuit:
    """Create a quantum circuit that implements the unitary oracle U_f for a given bitstring that encodes the balanced function f.
    The number of qubits, excluding a single ancilla qubit, is given by the length of the bitstring. """

    assert type(bitstring) == str
    assert len(bitstring)>0
    assert (bitstring.count('0')+bitstring.count('1'))==len(bitstring)

    n = len(bitstring)

    bo = QuantumCircuit(n+1) # "+1" for the ancilla qubit

    # Place X-gates
    for qubit in range(n):
        if bitstring[qubit] == '1':
            bo.x(qubit)

    # Use barrier as divider
    bo.barrier()

    # Controlled-NOT gates acting on ancilla (n-th qubit)
    for qubit in range(n):
        bo.cx(qubit, n)

    # Use barrier as divider
    bo.barrier()

    # Place X-gates again
    for qubit in range(n):
        if bitstring[qubit] == '1':
            bo.x(qubit)

    return bo


# Example usage:
balanced_oracle("101").draw()