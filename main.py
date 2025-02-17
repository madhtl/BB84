from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
eavesdropper_present = True
#both alice's and bob's bases values are my preference.
bits_no = 10
def prng(bits_no):
    return [random.randint(0,1) for _ in range(bits_no)]


alice_bits = prng(bits_no)
alice_bases = prng(bits_no)
alice_qubits = {}
for i in range(bits_no):
    alice_qubits[i] = {'bit': alice_bits[i], 'base': alice_bases[i]}
qr = QuantumRegister(bits_no)
cr = ClassicalRegister(bits_no)
qc = QuantumCircuit(qr, cr)

for i in range(bits_no):
    if alice_bits[i] == 1:
        qc.x(qr[i])
    if alice_bases[i] == 1:
        qc.h(qr[i])

#qc.draw('mpl')
#plt.show()
simulator = Aer.get_backend('qasm_simulator')

#changeable by the user
eavesdropper_present = False
if eavesdropper_present:
    eve_bases = prng(bits_no)
    qc.measure(qr, cr)
    qc_t = transpile(qc, simulator)
    job = simulator.run(qc_t, shots=1)

    result = job.result()
    counts = result.get_counts(qc)
    eve_measured_bits = list(counts.keys())[0]

    for i in range(bits_no):
        if int(eve_measured_bits[i]) == 1:
            qc.x(qr[i])
        if eve_bases[i] == 1:
            qc.h(qr[i])

bob_bases = prng(bits_no)
for i in range(bits_no):
    if bob_bases[i] == 1:
        qc.h(qr[i])

qc.measure(qr, cr)  # collapses qubit and stores it under cr

qc_t = transpile(qc, simulator)
job = simulator.run(qc_t, shots=1)
result = job.result()
counts = result.get_counts(qc)
bob_measured_bits = list(counts.keys())[0]
bob_measured_bits = [int(bit) for bit in bob_measured_bits]
print(bob_measured_bits)
message = []
eavesdropper_detected = False

for i in range(bits_no):
    if alice_bases[i] == bob_bases[i]:
        if bob_measured_bits[i] != alice_bits[i]:
            eavesdropper_detected = True
        message.append(alice_bits[i])

print(f"Alice sent:     {alice_bits}")
print(f"Alice's bases:  {alice_bases}")
print(f"Bob's bases:    {bob_bases}")
print(f"Bob received:   {bob_measured_bits}")
print(f"Final key:      {message}")
if eavesdropper_detected:
    print("Eavesdropper detected!")
else:
    print("No eavesdropper detected.")


#as we can see, even with the same instructions on qubits as Alice, Eve cannot replicate the state.





