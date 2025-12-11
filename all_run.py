# run_all.py
import time
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from all_lib import (
    build_database, train_rf,
    reduce_random_search, reduce_database_lookup, reduce_rf_lookup
)

def main():
    # Step 1: Build database (for V2, V3)
    db = build_database(depth=3)

    # Step 2: Train RF (for V3)
    try:
        clf = train_rf(db)
    except ImportError:
        clf = None
        print("⚠️ scikit-learn not installed. V3 will be skipped.")

    # Step 3: Example circuit
    qc = QuantumCircuit(1)
    qc.h(0); qc.h(0); qc.x(0); qc.h(0)
    print("Original Circuit:\n", qc)

    results = {}

    # V1
    start = time.time()
    red_v1 = reduce_random_search(qc)
    results["V1-RS"] = (red_v1, time.time() - start)

    # V2
    start = time.time()
    red_v2 = reduce_database_lookup(qc, db)
    results["V2-DR"] = (red_v2, time.time() - start)

    # V3
    if clf:
        start = time.time()
        red_v3 = reduce_rf_lookup(qc, db, clf)
        results["V3-RF"] = (red_v3, time.time() - start)

    # Print summary
    print("\n--- Results ---")
    for k, (circ, t) in results.items():
        print(f"{k}: {circ.size()} gates, time = {t:.4f} sec")

    # -------------------------------
    # Visualization
    # -------------------------------
    n = len(results) + 1  # Original + each method
    fig, axs = plt.subplots(1, n, figsize=(4*n, 3))

    # Original circuit
    qc.draw(output="mpl", ax=axs[0])
    axs[0].set_title(f"Original\n{qc.size()} gates")

    # Results
    for i, (k, (circ, t)) in enumerate(results.items(), start=1):
        circ.draw(output="mpl", ax=axs[i])
        axs[i].set_title(f"{k}\n{circ.size()} gates\n{t:.3f}s")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
