from guppylang.decorator import guppy
from guppylang.std.builtins import array, result
from guppylang.std.quantum import qubit, measure
from eris.steane import non_ft_zero
from .util import run, single_reg_counts

def test_non_ft_zero() -> None:
    @guppy
    def main() -> None:
        data_qubits = non_ft_zero()
        for q in data_qubits:
            result("c", measure(q))

    

    counts =single_reg_counts(run(guppy.get_module(), 7))
    print(counts)
    for bitsts in counts.keys():
        assert int(bitsts, 2) % 2 == 0