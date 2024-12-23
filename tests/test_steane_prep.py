from guppylang.decorator import guppy
from guppylang.std.builtins import array, result
from guppylang.std.quantum import qubit, measure
from eris.steane import non_ft_zero
from .util import run, single_reg_counts, even_parity


def permute_canonical(bitstr: str) -> str:
    map_from_canonical = {3: 0, 5: 1, 6: 2, 4: 3, 1: 4, 2: 5, 0: 6}

    return "".join(
        bitstr[map_from_canonical[i]] for i in range(len(map_from_canonical))
    )


def test_non_ft_zero() -> None:
    @guppy
    def main() -> None:
        data_qubits = non_ft_zero()
        for q in data_qubits:
            result("c", measure(q))

    counts = single_reg_counts(run(guppy.get_module(), 7, n_shots=100))
    bitsts = set(counts.keys())
    assert len(bitsts) == 8
    assert all(even_parity(bitstr) for bitstr in bitsts)

    # permute to canonical labelling of data qubits
    # https://errorcorrectionzoo.org/c/steane
    bitsts = {permute_canonical(bitstr) for bitstr in bitsts}
    assert bitsts == {
        "0000000",
        "1010101",
        "0110011",
        "1100110",
        "0001111",
        "1011010",
        "0111100",
        "1101001",
    }
