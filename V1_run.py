from qiskit import QuantumCircuit
from V1_lib import random_search_reduce, visualize_circuits

# ------------------------------
# Example circuit (7 qubits)
# ------------------------------
qc = QuantumCircuit(7)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 1)   # redundant (will cancel)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(2, 3)   # redundant (will cancel)
qc.cx(3, 4)
qc.cx(4, 5)
qc.cx(5, 6)
qc.h(6)


print("Original circuit depth:", qc.depth())

# Apply reduction
reduced_qc = random_search_reduce(qc, max_iters=30)
print("Reduced circuit depth:", reduced_qc.depth())

# Print textual representations
print("\nOriginal:")
print(qc)

print("\nReduced:")
print(reduced_qc)

# Show visual comparison
visualize_circuits(qc, reduced_qc)
