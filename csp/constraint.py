from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import Mapping
from typing import Self
from .state import State


@dataclass(frozen=True)
class Constraint[T](ABC):
    variables: frozenset[str]

    @classmethod
    def for_vars(cls, *vars: str) -> Self:
        return cls(frozenset(vars))

    def is_satisfied(self, state: State[T]) -> bool:
        return self.is_satisfied_with_partial(
            {
                name: var.value
                for name, var in state.items()
                if name in self.variables and var.value is not None
            }
        )

    @abstractmethod
    def is_satisfied_with_partial(self, assignment: Mapping[str, T]) -> bool:
        """Return True if the constraint is satisfied under a partial assignment."""
