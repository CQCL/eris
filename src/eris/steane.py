from typing import no_type_check
from guppylang.decorator import guppy
from guppylang.std.builtins import array, owned
from guppylang.std import quantum as phys


@guppy.struct
@no_type_check
# TODO is it confusing to shadow the name of qubit?
class qubit:
    data_qs: array[phys.qubit, 7]



@guppy
@no_type_check
def non_ft_zero() -> qubit:
    data_qubits = array(phys.qubit() for _ in range(7))
    plus_ids = array(0, 4, 6)
    for i in plus_ids:
        phys.h(data_qubits[i])

    cx_pairs = array((0, 1), (4, 5), (6, 3), (6, 5), (4, 2), (0, 3), (4, 1), (3, 2))
    for c, t in cx_pairs:
        phys.cx(data_qubits[c], data_qubits[t])
    return qubit(data_qubits)


@guppy
@no_type_check
def ft_zero() -> tuple[qubit, bool]:
    q = non_ft_zero()
    # TODO compilation barrier
    ancilla = phys.qubit()
    flags = array(1, 3, 5)
    for f in flags:
        phys.cx(q.data_qs[f], ancilla)
    return q, phys.measure(ancilla)


@guppy
@no_type_check
def ft_zero_attempts(attempts: int) -> qubit:
    """Attempt fault-tolerant zero preparation multiple times,
    until success or the maximum number of attempts is reached.
    """
    q, failed = ft_zero()
    for _ in range(attempts - 1):
        if not failed:
            break
        discard(q)
        q, failed = ft_zero()
    return q

@guppy
@no_type_check
def h(q: qubit) -> None:
    for i in range(len(q.data_qs)):
        phys.h(q.data_qs[i])

@guppy
@no_type_check
def x(q: qubit) -> None:
    for i in range(len(q.data_qs)):
        phys.x(q.data_qs[i])


@guppy
@no_type_check
def z(q: qubit) -> None:
    for i in range(len(q.data_qs)):
        phys.z(q.data_qs[i])


@guppy
@no_type_check
def cx(ctrl: qubit, tgt: qubit) -> None:
    for i in range(len(ctrl.data_qs)):
        phys.cx(ctrl.data_qs[i], tgt.data_qs[i])


@guppy
@no_type_check
def measure(q: qubit @ owned) -> bool:
    return parity_check(phys.measure_array(q.data_qs))


@guppy
@no_type_check
def discard(q: qubit @ owned) -> None:
    phys.discard_array(q.data_qs)


n = guppy.nat_var("n")


@guppy
@no_type_check
def parity_check(data_bits: array[bool, n]) -> bool:
    # TODO use xor
    out = 0
    for b in data_bits:
        out += int(b)
    return out % 2 == 1
