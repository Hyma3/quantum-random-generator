import argparse
import os
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

IMG_DIR = "images"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

#build a quantum circuit in order to draw it
def build_circuit(nb_qubits):
    qc = QuantumCircuit(nb_qubits)
    qc.h(range(nb_qubits))
    qc.measure_all()
    return qc

#draw and save the quantum circuit image
def draw_and_save(nb_qubits):
    file_name = os.path.join(IMG_DIR, f"quantum_circuit_{nb_qubits}_qubits.png")
    print(f"Loading quantum circuit image for {nb_qubits}...")
    qc = build_circuit(nb_qubits)
    qc.draw('mpl', filename=file_name)
    print(f"Quantum circuit image saved as {file_name}.")

#generate a random number using quantum computing
def generator_quantum_number(min_val, max_val):
    #we calculate the number of qubits needed to cover the range
    range_size = max_val - min_val + 1
    num_qubits = range_size.bit_length()

    #we create a quantum circuit with the necessary number of qubits
    circuit = QuantumCircuit(num_qubits)

    #we apply a Hadamard gate to each qubit to create a uniform superposition
    circuit.h(range(num_qubits))

    #we measure the qubits
    circuit.measure_all()

    #we simulate the quantum circuit
    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1, memory=True).result()

    #we retrieve the measurement result
    measurement = result.get_memory()[0]

    #we convert the binary result to an integer
    decimal_number = int(measurement, 2)

    if decimal_number >= range_size:
        return generator_quantum_number(min_val, max_val)  # we restart the generation if out of range

    return min_val + decimal_number

#benchmark the quantum random number generator
def benchmark(min_val, max_val, iterations=1000):
    print(f"Benchmarking quantum random number generator for {iterations} iterations between {min_val} and {max_val}...")
    dataset = []
    for i in range(iterations):
        random_number = generator_quantum_number(min_val, max_val)
        dataset.append(random_number)

    plt.figure(figsize=(10, 6))

    nb_bins = max_val - min_val + 1
    plt.hist(dataset, bins=nb_bins, color='skyblue', edgecolor='black', alpha=0.7)

    plt.title(f'Quantum Random Number Generator Distribution ({iterations} samples)', fontsize=16)
    plt.xlabel('Random Number', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', alpha=0.5)

    name_image = os.path.join(IMG_DIR, f"benchmark_quantum_{iterations}.png")
    plt.savefig(name_image)
    print(f"Benchmark histogram saved as {name_image}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a random number using quantum computing and save the quantum circuit image.",
        epilog="Example usage: python rng_quantique.py --min 1 --max 10 --image"
    )

    parser.add_argument("--min", type=int, default=0, help="Minimum value of the range (inclusive). Default is 0.")
    parser.add_argument("--max", type=int, default=100, help="Maximum value of the range (inclusive). Default is 100.")
    parser.add_argument("-i","--image", action="store_true", help="If set, saves the quantum circuit image as 'quantum_circuit.png'.")
    parser.add_argument("-q","--qubits", type=int, default=4, help="Number of qubits for the quantum circuit image. Default is 4.")
    parser.add_argument("-b","--benchmark", action="store_true", help="If set, runs a benchmark and saves the histogram as 'benchmark_quantum_rng.png'. 1000 iterations by default.")
    parser.add_argument("-it","--iterations", type=int, default=1000, help="Number of iterations for the benchmark. Default is 1000.")
    args = parser.parse_args()

    print("Starting quantum random number generation...")

    if args.min >= args.max:
        print("Error: Minimum value must be less than maximum value.")
        exit(1)

    if args.image:
        draw_and_save(args.qubits)

    if args.benchmark:
        benchmark(args.min, args.max, args.iterations)
    else : 
        try:
            print(f"Generating a random number between {args.min} and {args.max}...")
            random_number = generator_quantum_number(args.min, args.max)
            print(f"Generated random number: {random_number}")
        except Exception as e:
            print(f"An error occurred during random number generation: {e}")