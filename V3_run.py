# run_rf_optimizer.py
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from V3_lib import build_database, train_rf, reduce_circuit_rf

def main():
    # Step 1: Build database
    db = build_database(depth=3)

    # Step 2: Train random forest
    clf = train_rf(db)

    # Step 3: Create test circuit
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.h(0)
    qc.x(0)
    qc.h(0)

    print("Original circuit:")
    print(qc)

    # Step 4: Reduce with RF prefilter
    reduced = reduce_circuit_rf(qc, db, clf)

    print("\nReduced circuit:")
    print(reduced)

    # Step 5: Visualize
    fig, axs = plt.subplots(1, 2, figsize=(10, 3))
    qc.draw(output="mpl", ax=axs[0])
    axs[0].set_title("Original Circuit")
    reduced.draw(output="mpl", ax=axs[1])
    axs[1].set_title("Reduced Circuit (V3-RF)")
    plt.show()

if __name__ == "__main__":
    main()
