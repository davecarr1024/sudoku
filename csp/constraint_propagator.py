from abc import ABC, abstractmethod
from dataclasses import dataclass
from .csp import CSP
from .state import State


@dataclass(frozen=True)
class ConstraintPropagator[T](ABC):
    @abstractmethod
    def propagate(self, csp: CSP[T], state: State[T]) -> State[T] | None: ...
