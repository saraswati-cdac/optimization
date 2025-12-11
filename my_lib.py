# my_qiskit_lib.py

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime.fake_provider import FakeAthensV2

def create_circuit():
    """Create the original quantum circuit."""
    qc = QuantumCircuit(3)
    qc.cx(0, 2)
    return qc

def get_backend():
    """Return the fake Athens backend."""
    return FakeAthensV2()

def transpile_circuit(circuit, backend, optimization_level=0):
    """Transpile the circuit for a given backend and optimization level."""
    return transpile(circuit, backend, optimization_level=optimization_level)

def draw_circuit(circuit):
    """Return the text representation of a circuit."""
    return circuit.draw(output="text")
 