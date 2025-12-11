# run_optimizer.py
from qiskit import QuantumCircuit
from V2_lib import build_database, reduce_circuit
import matplotlib.pyplot as plt

def main():
    # Step 1: Build database
    db = build_database(depth=3)

    # Step 2: Create a test circuit
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.h(0)
    qc.x(0)
    qc.h(0)

    print("Original circuit:")
    print(qc)

    # Step 3: Reduce circuit
    reduced = reduce_circuit(qc, db)

    print("\nReduced circuit:")
    print(reduced)

    # Step 4: Visualization
    fig, axs = plt.subplots(1, 2, figsize=(10, 3))
    qc.draw(output="mpl", ax=axs[0])
    axs[0].set_title("Original Circuit")
    reduced.draw(output="mpl", ax=axs[1])
    axs[1].set_title("Reduced Circuit")
    plt.show()

if __name__ == "__main__":
    main()
