from abc import ABC, abstractmethod
from dataclasses import dataclass
from .state import State


@dataclass(frozen=True)
class Constraint[T](ABC):
    variables: frozenset[str]

    @abstractmethod
    def is_satisfied(self, state: State[T]) -> bool: ...
