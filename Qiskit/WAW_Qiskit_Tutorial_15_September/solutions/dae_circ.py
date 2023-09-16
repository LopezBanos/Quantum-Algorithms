# ==Solution==
from qiskit import QuantumCircuit
import qiskit_aer

import numpy as np

def dense_angle_enc(x: np.ndarray | list[float]) -> QuantumCircuit:
    xvec = np.asarray(x)
    assert len(xvec.shape) == 1
    Nx = xvec.shape[0]
    Nx = int(Nx // 1 + 1)

    daqc = QuantumCircuit(int(Nx/2))

    for i in range(int(Nx/2)):
        daqc.u(2*(xvec[2*i-1]), xvec[2*i], 0 , i)

    return daqc

# Example usage:
qc = dense_angle_enc([np.pi/2 , np.pi/4])
#qc.draw()
qiskit_aer.quantum_info.AerStatevector(qc, method='statevector').draw('latex')