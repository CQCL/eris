from collections import Counter
from typing import no_type_check
from guppylang.decorator import guppy
from guppylang.std.builtins import result
from guppylang.std import quantum as gq
from eris.steane import non_ft_zero, x, ft_zero, ft_zero_attempts, cx, measure, discard
from .util import run, single_reg_counts


def permute_canonical(bitstr: str) -> str:
    map_from_canonical = {3: 0, 5: 1, 6: 2, 4: 3, 1: 4, 2: 5, 0: 6}

    return "".join(
        bitstr[map_from_canonical[i]] for i in range(len(map_from_canonical))
    )


def flip_bits(bitstr: str) -> str:
    return "".join("1" if b == "0" else "0" for b in bitstr)


ZERO_BASES = {
    "0000000",
    "1010101",
    "0110011",
    "1100110",
    "0001111",
    "1011010",
    "0111100",
    "1101001",
}


def is_zero(counts: Counter[str]) -> bool:
    bitsts = set(counts.keys())
    # permute to canonical labelling of data qubits
    # https://errorcorrectionzoo.org/c/steane
    bitsts = {permute_canonical(bitstr) for bitstr in bitsts}

    return bitsts == ZERO_BASES


def is_one(counts: Counter[str]) -> bool:
    bitsts = set(counts.keys())
    one_bases = {flip_bits(b) for b in ZERO_BASES}
    return {permute_canonical(bitstr) for bitstr in bitsts} == one_bases


def test_non_ft_zero() -> None:
    @guppy
    @no_type_check
    def main() -> None:
        steane_q = non_ft_zero()
        for q in steane_q.data_qs:
            result("zero", gq.measure(q))

        steane_q = non_ft_zero()
        x(steane_q)
        for q in steane_q.data_qs:
            result("one", gq.measure(q))

    results = run(guppy.get_module(), 7, n_shots=100, random_seed=1)
    assert is_zero(single_reg_counts(results, "zero"))

    # test X gate
    assert is_one(single_reg_counts(results, "one"))


def test_ft_zero() -> None:
    @guppy
    @no_type_check
    def main() -> None:
        steane_q, goto = ft_zero()
        for q in steane_q.data_qs:
            result("ft_zero", gq.measure(q))

        result("goto", goto)

    results = run(guppy.get_module(), 8, n_shots=100, random_seed=2)
    assert is_zero(single_reg_counts(results, "ft_zero"))
    # TODO test with error model
    assert single_reg_counts(results, "goto") == {"0": 100}


def test_ft_zero_attempts() -> None:
    @guppy
    @no_type_check
    def main() -> None:
        steane_q = ft_zero_attempts(3)
        result("res", measure(steane_q))

    results = run(guppy.get_module(), 8, n_shots=100, random_seed=2)
    assert single_reg_counts(results, "res") == {"0": 100}


def test_cx() -> None:
    @guppy
    @no_type_check
    def main() -> None:
        c = non_ft_zero()
        t = non_ft_zero()
        x(c)
        cx(c, t)
        result("t", measure(t))
        discard(c)

    results = run(guppy.get_module(), 14, n_shots=100, random_seed=3)
    assert single_reg_counts(results, "t") == {"1": 100}
