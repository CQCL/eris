from guppylang.decorator import guppy
from guppylang.std.builtins import array
from guppylang.std.quantum import qubit
from guppylang.std import quantum as gq


@guppy
def non_ft_zero() -> array[qubit, 7]:
    data_qubits = array(qubit() for _ in range(7))
    plus_ids = array(0, 4, 6)
    # plus_ids = array(0, 1, 2)
    for i in plus_ids:
        gq.h(data_qubits[i])

    cx_pairs = array((0, 1), (4, 5), (6, 3), (6, 5), (4, 2), (0, 3), (4, 1), (3, 2))
    # cx_pairs = array(
    #     (6, 4),
    #     (6, 5),
    #     (0, 3),
    #     (1, 3),
    #     (0, 5),
    #     (2, 3),
    #     (1, 4),
    #     (0, 6),
    #     (2, 4),
    #     (1, 6),
    #     (2, 5),
    # )
    for c, t in cx_pairs:
        gq.cx(data_qubits[c], data_qubits[t])
    return data_qubits
