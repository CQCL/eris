from guppylang.decorator import guppy
from guppylang.std.builtins import array
from guppylang.std import quantum as phys

# @guppy
# class Steane:
#     data_qs: array[phys.qubit, 7]

@guppy
def non_ft_zero() -> array[phys.qubit, 7]:
    data_qubits = array(phys.qubit() for _ in range(7))
    plus_ids = array(0, 4, 6)
    for i in plus_ids:
        phys.h(data_qubits[i])

    cx_pairs = array((0, 1), (4, 5), (6, 3), (6, 5), (4, 2), (0, 3), (4, 1), (3, 2))
    for c, t in cx_pairs:
        phys.cx(data_qubits[c], data_qubits[t])
    return data_qubits


@guppy
def ft_zero() -> tuple[array[phys.qubit, 7], bool]:
    data_qubits = non_ft_zero()
    # TODO compilation barrier
    ancilla = phys.qubit()
    flags = array(1, 3, 5)
    for f in flags:
        phys.cx(data_qubits[f], ancilla)
    return data_qubits, phys.measure(ancilla)


@guppy
def ft_zero_attempts(attempts: int) -> array[phys.qubit, 7]:
    """Attempt fault-tolerant zero preparation multiple times,
    until success or the maximum number of attempts is reached.
    """
    data_qubits, failed = ft_zero()
    for _ in range(attempts - 1):
        if not failed:
            break
        phys.discard_array(data_qubits)
        data_qubits, failed = ft_zero()
    return data_qubits


@guppy
def x(data_qubits: array[phys.qubit, 7]) -> None:
    for i in range(len(data_qubits)):
        phys.x(data_qubits[i])


@guppy
def z(data_qubits: array[phys.qubit, 7]) -> None:
    for i in range(len(data_qubits)):
        phys.z(data_qubits[i])


@guppy
def cx(ctrl: array[phys.qubit, 7], tgt: array[phys.qubit, 7]) -> None:
    for i in range(len(ctrl)):
        phys.cx(ctrl[i], tgt[i])


n = guppy.nat_var("n")
@guppy
def parity_check(data_bits: array[bool, n]) -> bool:
    # TODO use xor
    out = 0
    for b in data_bits:
        out += int(b)
    return out % 2 == 1
