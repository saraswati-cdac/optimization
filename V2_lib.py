from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

# small gate set
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

def reduce_circuit(circuit, db):
    """Replace with shortest equivalent circuit from database."""
    reduced = QuantumCircuit(1)
    for gate, _, _ in circuit.data:
        temp = reduced.copy()
        getattr(temp, gate.name)(0)
        key = unitary_key(temp)
        reduced = db.get(key, temp).copy()
    return reduced
