# run_qiskit.py

from my_lib import create_circuit, get_backend, transpile_circuit, draw_circuit

def main():
    # Create original circuit
    qc = create_circuit()
    print("Original circuit:")
    print(draw_circuit(qc))

    # Get backend
    backend = get_backend()

    # Transpile without optimization
    no_opt = transpile_circuit(qc, backend, optimization_level=0)
    print("\nCircuit without optimization:")
    print(draw_circuit(no_opt))

    # Transpile with optimization
    opt = transpile_circuit(qc, backend, optimization_level=3)
    print("\nCircuit with optimization:")
    print(draw_circuit(opt))

if __name__ == "__main__":
    main()
    
