from guppylang.decorator import guppy
from guppylang.std.builtins import array
from guppylang.std.quantum import qubit
from guppylang.std import quantum as gq


@guppy
def non_ft_zero() -> array[qubit, 7]:
    data_qubits = array(qubit() for _ in range(7))
    plus_ids = array(0, 4, 6)
    for i in plus_ids:
        gq.h(data_qubits[i])

    cx_pairs = array((0, 1), (4, 5), (6, 3), (6, 5), (4, 2), (0, 3), (4, 1), (3, 2))
    for c, t in cx_pairs:
        gq.cx(data_qubits[c], data_qubits[t])
    return data_qubits


@guppy
def ft_zero() -> tuple[array[qubit, 7], bool]:
    data_qubits = non_ft_zero()
    # TODO compilation barrier
    ancilla = qubit()
    flags = array(1, 3, 5)
    for f in flags:
        gq.cx(data_qubits[f], ancilla)
    return data_qubits, gq.measure(ancilla)


@guppy
def x(data_qubits: array[qubit, 7]) -> None:
    for i in range(len(data_qubits)):
        gq.x(data_qubits[i])


@guppy
def z(data_qubits: array[qubit, 7]) -> None:
    for i in range(len(data_qubits)):
        gq.z(data_qubits[i])


@guppy
def cx(ctrl: array[qubit, 7], tgt: array[qubit, 7]) -> None:
    for i in range(len(ctrl)):
        gq.cx(ctrl[i], tgt[i])
