from .csp import CSP
from .state import State
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Propagator[T](ABC):
    @dataclass
    class Stats:
        domain_prunes: int = 0
        constraint_checks: int = 0

        def __add__(self, rhs: "Propagator.Stats") -> "Propagator.Stats":
            return Propagator.Stats(
                domain_prunes=self.domain_prunes + rhs.domain_prunes,
                constraint_checks=self.constraint_checks + rhs.constraint_checks,
            )

    @dataclass
    class Result:
        stats: "Propagator.Stats" = field(default_factory=lambda: Propagator.Stats())
        success: bool = True

    @abstractmethod
    def propagate(self, csp: CSP[T], state: State[T]) -> "Propagator.Result": ...
