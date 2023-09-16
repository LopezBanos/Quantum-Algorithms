def djqc(oracle: QuantumCircuit) -> QuantumCircuit:
    # Infer number of qubits excluding the ancilla:
    n = len(oracle.qubits)-1

    # Create a quantum circuit including the ancilla and classical registers
    dj_circ = QuantumCircuit(n+1,n)

    # Put ancilla qubit in state |1> by applying Pauli-X
    dj_circ.x(n)
    dj_circ.barrier()

    # Apply H-gates
    for qubit in range(n+1):
        dj_circ.h(qubit)

    # Add oracle
    dj_circ.barrier()
    dj_circ=dj_circ.compose(oracle)

    # Repeat H-gates
    dj_circ.barrier()
    for qubit in range(n):
        dj_circ.h(qubit)
    dj_circ.barrier()

    # Measure |x>
    for i in range(n):
        dj_circ.measure(i, i)

    return dj_circ