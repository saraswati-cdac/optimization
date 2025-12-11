noise_model = NoiseModel()

# Example depolarizing errors for 1- and 2-qubit gates
single_qubit_error = depolarizing_error(0.02, 1)
two_qubit_error = depolarizing_error(0.05, 2)

# Add noise to common operations
noise_model.add_all_qubit_quantum_error(single_qubit_error, ['h', 'rx', 'ry', 'rz'])
noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx'])

print("\n✅ Noise model is ACTIVE")
for i, e in enumerate(noise_model.to_dict()['errors']):
    print(f"  Error {i+1}: {e['operations']} -> Type: {e['type']}")
