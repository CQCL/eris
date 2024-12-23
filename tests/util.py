from collections import Counter
from guppylang.hresult import HShots
from guppylang.module import GuppyModule
from hsim import build_hsim
from hsim.backends import SimBackend, Stim


def run(
    module: GuppyModule,
    n_qubits: int,
    n_shots: int = 10,
    backend: SimBackend | None = None,
    random_seed: int = 12,
    test_name: str = "test",
) -> HShots:
    """Executes a quantum simulation run with the specified parameters.

    Args:
        module (GuppyModule): The quantum module to be simulated.
        n_qubits (int): The number of qubits to be used in the simulation.
        n_shots (int, optional): The number of shots (repetitions) for the simulation.
            Defaults to 10.
        backend (SimBackend | None, optional): The simulation backend to be used.
            If None, a default backend with the specified random seed is used.
            Defaults to None.
        random_seed (int, optional): The random seed for the simulation backend.
            Defaults to 12.
        test_name (str, optional): The name of the test being run. Defaults to "test".

    Returns:
        HShots: The result of the simulation run, containing the shots data.
    """
    backend = backend or Stim(random_seed=random_seed)
    runner = build_hsim(module.compile().package, test_name)
    return HShots(runner.run_shots(backend, n_qubits=n_qubits, n_shots=n_shots))


def single_reg_counts(shots: HShots, reg: str = "c") -> Counter[str]:
    c = Counter()
    for pairs, val in shots.collated_counts().items():
        for reg_name, bits in pairs:
            if reg_name == reg:
                c[bits] += val
    return c
