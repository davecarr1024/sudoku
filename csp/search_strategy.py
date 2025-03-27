from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
from .state import State
from .constraint_propagator import ConstraintPropagator
from .solver_stats import SolverStats
from .csp import CSP


@dataclass(frozen=True)
class SearchStrategy[T](ABC):
    propagator: ConstraintPropagator[T]

    @abstractmethod
    def solve(
        self, csp: CSP[T], state: State[T]
    ) -> tuple[SolverStats, Optional[State[T]]]: ...
