# circuit_optimizer_rf.py
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np
from collections import deque
from sklearn.ensemble import RandomForestClassifier  #--> scikit-learn (the library that provides RandomForestClassifier

# Small gate set
gates = {
    "x": lambda qc: qc.x(0),
    "h": lambda qc: qc.h(0)
}

def unitary_key(circuit):
    """Hashable key for a circuit's unitary (ignores global phase)."""
    U = Operator(circuit).data
    phase = np.exp(-1j * np.angle(np.linalg.det(U)) / U.shape[0])
    return np.round(U * phase, 5).tobytes()

def build_database(depth=3):
    """Return dictionary mapping unitaries to shortest circuits."""
    db = {}
    queue = deque([QuantumCircuit(1)])
    while queue:
        qc = queue.popleft()
        key = unitary_key(qc)
        if key not in db or qc.size() < db[key].size():
            db[key] = qc.copy()
        if qc.size() < depth:
            for g in gates.values():
                new_qc = qc.copy()
                g(new_qc)
                queue.append(new_qc)
    return db

def extract_features(circuit):
    """Simple feature vector for ML model."""
    return [
        circuit.size(),
        sum(1 for g, _, _ in circuit.data if g.name == "x"),
        sum(1 for g, _, _ in circuit.data if g.name == "h"),
    ]

def train_rf(db):
    """Train RandomForest to classify reducible vs irreducible circuits."""
    X, y = [], []
    for key, qc in db.items():
        # Feature vector
        feat = extract_features(qc)
        X.append(feat)
        # Reducible if smaller than original size (dummy criterion)
        y.append(1 if qc.size() > 1 else 0)  # 1 = reducible, 0 = irreducible
    clf = RandomForestClassifier(n_estimators=20, random_state=0)
    clf.fit(X, y)
    return clf

def reduce_circuit_rf(circuit, db, clf):
    """Reduce circuit with random forest prefilter + database lookup."""
    reduced = QuantumCircuit(1)
    for gate, _, _ in circuit.data:
        temp = reduced.copy()
        getattr(temp, gate.name)(0)
        key = unitary_key(temp)

        # Use RF to decide if lookup is worth it
        features = [extract_features(temp)]
        if clf.predict(features)[0] == 1:  # Reducible
            reduced = db.get(key, temp).copy()
        else:
            reduced = temp.copy()
    return reduced
