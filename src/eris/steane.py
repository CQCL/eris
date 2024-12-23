from guppylang.decorator import guppy
from guppylang.std.builtins import array
from guppylang.std.quantum import qubit


@guppy
def non_ft_zero() -> array[qubit, 7]:
    data_qubits = array(qubit() for _ in range(7))

    # TODO do the prep

    return data_qubits