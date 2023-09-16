For our implementation we can use the single-qubit unitary rotation gate in qiskit (see [here](https://qiskit.org/documentation/tutorials/circuits/3_summary_of_quantum_operations.html#Single-Qubit-Gates) for documentation):

$\begin{equation}
\begin{split}U(\theta, \phi, \lambda) =
    \begin{pmatrix}
        \cos\left(\frac{\theta}{2}\right)          & -e^{i\lambda}\sin\left(\frac{\theta}{2}\right) \\
        e^{i\phi}\sin\left(\frac{\theta}{2}\right) & e^{i(\phi+\lambda)}\cos\left(\frac{\theta}{2}\right)
    \end{pmatrix}\end{split}
\end{equation}$

Note that this matrix refers to the basis given by $(1,0)^T = |0\rangle $ and $(0,1)^T = |1\rangle $.