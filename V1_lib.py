import random
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

# ------------------------------
# Helper functions
# ------------------------------

def random_subsequence(circuit, length):
    """Pick a random subsequence of given length."""
    if length > len(circuit):
        return None, None
    start = random.randint(0, len(circuit) - length)
    end = start + length
    return start, end

def is_equivalent(circ1, circ2, tol=1e-5):
    """Check unitary equivalence up to global phase."""
    U1 = Operator(circ1).data
    U2 = Operator(circ2).data
    diff = np.allclose(U1, U2, atol=tol) or np.allclose(U1, -U2, atol=tol)
    return diff

# ------------------------------
# Random Search Reduction (V1)
# ------------------------------

def random_search_reduce(circuit, max_iters=20):
    qc = circuit.copy()
    for it in range(max_iters):
        if len(qc.data) < 2:
            break

        # Pick random subsequence of length n
        n = random.randint(2, min(5, len(qc.data)))
        start, end = random_subsequence(qc.data, n)
        if start is None:
            continue

        # Build subsequence circuit
        subc = QuantumCircuit(qc.num_qubits)
        for instr, qargs, cargs in qc.data[start:end]:
            subc.append(instr, qargs, cargs)

        # --- Candidate shorter subsequence ---
        cand = None

        # First try identity (empty subsequence)
        empty_cand = QuantumCircuit(qc.num_qubits)
        if is_equivalent(subc, empty_cand):
            cand = empty_cand
        else:
            # Otherwise try random shorter sequence
            p = random.randint(1, n - 1)
            cand = QuantumCircuit(qc.num_qubits)
            for _ in range(p):
                q1, q2 = random.sample(range(qc.num_qubits), 2)
                gate = random.choice(["cx", "cz"])
                if gate == "cx":
                    cand.cx(q1, q2)
                else:
                    cand.cz(q1, q2)

        # Compare and replace if equivalent
        if is_equivalent(subc, cand):
            new_qc = QuantumCircuit(qc.num_qubits)

            # Copy prefix
            for instr, qargs, cargs in qc.data[:start]:
                new_qc.append(instr, qargs, cargs)

            # Insert candidate (gate-by-gate)
            for instr, qargs, cargs in cand.data:
                new_qc.append(instr, qargs, cargs)

            # Copy suffix
            for instr, qargs, cargs in qc.data[end:]:
                new_qc.append(instr, qargs, cargs)

            print(f"Iteration {it}: replacing gates {start}:{end} "
                  f"(len {len(subc.data)}) with shorter sequence (len {len(cand.data)})")

            qc = new_qc

    return qc


# ------------------------------
# Visualization
# ------------------------------

def visualize_circuits(original, reduced):
    """Show side-by-side circuit diagrams."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    original.draw("mpl", ax=axes[0])
    reduced.draw("mpl", ax=axes[1])
    axes[0].set_title("Original Circuit")
    axes[1].set_title("Reduced Circuit")
    plt.tight_layout()
    plt.show()
