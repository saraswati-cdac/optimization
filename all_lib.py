# ckt_optimizer.py
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np
import random
from collections import deque

# For V3
try:
    from sklearn.ensemble import RandomForestClassifier
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# -------------------------
# Helpers
# -------------------------
gates = {
    "x": lambda qc: qc.x(0),
    "h": lambda qc: qc.h(0)
}

def unitary_key(circuit):
    """Hashable key for a circuit's unitary (ignores global phase)."""
    U = Operator(circuit).data
    phase = np.exp(-1j * np.angle(np.linalg.det(U)) / U.shape[0])
    return np.round(U * phase, 5).tobytes()

def extract_features(circuit):
    """Simple features for ML classifier."""
    return [
        circuit.size(),
        sum(1 for g, _, _ in circuit.data if g.name == "x"),
        sum(1 for g, _, _ in circuit.data if g.name == "h"),
    ]


# -------------------------
# V1: Random Search
# -------------------------
def reduce_random_search(circuit, max_trials=100):
    """Naive random search for shorter equivalent circuits."""
    best = circuit.copy()
    for _ in range(max_trials):
        if best.size() < 2:
            break
        # Pick random subsequence
        start = random.randint(0, best.size() - 1)
        end = random.randint(start + 1, best.size())
        sub = QuantumCircuit(1)
        for g, _, _ in best.data[start:end]:
            getattr(sub, g.name)(0)

        # Try random replacement of shorter length
        for _ in range(5):
            trial = QuantumCircuit(1)
            for _ in range(random.randint(0, max(0, sub.size() - 1))):
                random.choice(list(gates.values()))(trial)
            if np.allclose(Operator(trial).data, Operator(sub).data, atol=1e-5):
                # Replace in circuit
                new_qc = QuantumCircuit(1)
                for g, _, _ in best.data[:start]:
                    getattr(new_qc, g.name)(0)
                for g, _, _ in trial.data:
                    getattr(new_qc, g.name)(0)
                for g, _, _ in best.data[end:]:
                    getattr(new_qc, g.name)(0)
                if new_qc.size() < best.size():
                    best = new_qc
    return best


# -------------------------
# V2: Database Retrieval
# -------------------------
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

def reduce_database_lookup(circuit, db):
    """Reduce circuit using precomputed database lookups."""
    reduced = QuantumCircuit(1)
    for gate, _, _ in circuit.data:
        reduced_copy = reduced.copy()
        getattr(reduced_copy, gate.name)(0)
        key = unitary_key(reduced_copy)
        reduced = db.get(key, reduced_copy).copy()
    return reduced


# -------------------------
# V3: Random Forest + DB
# -------------------------
def train_rf(db):
    """Train RandomForest classifier to predict reducibility."""
    if not HAS_SKLEARN:
        raise ImportError("scikit-learn not installed. Run: pip install scikit-learn")
    X, y = [], []
    for key, qc in db.items():
        feat = extract_features(qc)
        X.append(feat)
        y.append(1 if qc.size() > 1 else 0)  # reducible if size > 1
    clf = RandomForestClassifier(n_estimators=20, random_state=0)
    clf.fit(X, y)
    return clf

def reduce_rf_lookup(circuit, db, clf):
    """Reduce circuit with RF prefilter + database lookup."""
    reduced = QuantumCircuit(1)
    for gate, _, _ in circuit.data:
        temp = reduced.copy()
        getattr(temp, gate.name)(0)
        key = unitary_key(temp)
        features = [extract_features(temp)]
        if clf.predict(features)[0] == 1:
            reduced = db.get(key, temp).copy()
        else:
            reduced = temp.copy()
    return reduced
