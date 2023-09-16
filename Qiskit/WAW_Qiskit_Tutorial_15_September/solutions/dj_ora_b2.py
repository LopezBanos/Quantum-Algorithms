# ==Solution==

from IPython.display import Latex
from qiskit.visualization import state_visualization
from qiskit.quantum_info import Statevector

bo = balanced_oracle("101")
#print(bo.draw())

prefix = "$$\\begin{align}"
suffix = "\\end{align}$$"
strlat = ""

for i in range(2**3):
    state = Statevector.from_int(i, 2**(3+1))
    state_to_latex = state_visualization._state_to_latex_ket(state.data, max_size = 128)
    strlat = strlat + state_to_latex + "\mapsto"

    state = state.evolve(bo)
    state_to_latex = state_visualization._state_to_latex_ket(state.data, max_size = 128)
    strlat = strlat + state_to_latex + "\\nonumber" +  "\\\ "

Latex(prefix + strlat + suffix)

# Careful: Qiskit uses the reverse ordering of qubits!
# E.g. |q_3 q_2 q_1 q_0> instead of |q_0 q_1 q_2 q_3>
# If q_3 is the ancilla, it is thus appearing as the leftmost entry.
# See: https://qiskit.org/documentation/tutorials/circuits/3_summary_of_quantum_operations.html#Basis-vector-ordering-in-Qiskit