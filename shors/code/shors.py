import numpy as np
from numpy import pi
from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ
from qiskit.providers.aer import QasmSimulator
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram, plot_bloch_multivector


def plot_bloch(qc):
    """Simulates qc and displays the resulting state in bloch spheres"""
    sv_sim = Aer.get_backend("statevector_simulator")
    qobj = assemble(qc)
    statevector = sv_sim.run(qobj).result().get_statevector()
    plot_bloch_multivector(statevector)


def qft_rotations(circuit, n):
    """Recursively performs rotations on the circuit"""
    if n == 0:  # Empty circuit
        return circuit
    n -= 1  # Indexes start from 0
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi / 2 ** (n - qubit), qubit, n)

    # At the end of the function, recurse for the next qubits
    qft_rotations(circuit, n)


def swap_registers(circuit, n):
    """For a given circuit of even length n, performs swaps of outermost qubits, moving in."""
    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)
    return circuit


def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit


def inverse_qft(circuit, n):
    """Does the inverse QFT on the first n qubits in circuit"""
    # Create QFT circuit
    qft_circ = qft(QuantumCircuit(n), n)
    # Inverse it
    inv_qft_circ = qft_circ.inverse()
    # Add it to the first n qubits of circuit
    circuit.append(inv_qft_circ, circuit.qubits[:n])
    return circuit.decompose()  # decompose() allows us to see the individual gates


def h_all(qc, n):
    """Applies the H gate to first n qubits in the circuit"""
    for qubit in range(n):
        qc.h(qubit)

    return qc


def simulate(qc, shots=1024):
    """Simulates the given circuit and returns the counts from the results"""
    simulator = QasmSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=2048)
    result = job.result()
    counts = result.get_counts(qc)
    return counts


def prepare_circuit(nqubits=3, number=5):
    """Creates a quantum circuit and encodes the number in phase rotations"""
    qc = QuantumCircuit(nqubits)
    qc = h_all(qc, nqubits)

    qc.p(number * pi / 4, 0)
    qc.p(number * pi / 2, 1)
    qc.p(number * pi, 2)

    qc = inverse_qft(qc, nqubits)
    qc.measure_all()

    return qc


def qft_dagger(qc, n):
    """n-qubit QFTdagger the first n qubits in circuit"""
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for i in range(n):
        for j in range(i):
            qc.cp(-pi / float(2 ** (i - j)), j, i)
        qc.h(i)


def qpe(qc, n, angle):
    """Applies quantum phase estimation for the given circuit qc of length n at the given angle."""
    qc = h_all(qc, n)
    qc.x(n)

    reps = 1
    for counter in range(n):
        for i in range(reps):
            qc.cp(angle, counter, n)
        reps = reps * 2

    qc = inverse_qft(qc, n)
    for i in range(n):
        qc.measure(i, i)

    return qc
