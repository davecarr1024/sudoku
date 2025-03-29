from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self
from functools import cache
from .state import State

type Assignment[T] = frozenset[tuple[str, T]]


@dataclass(frozen=True)
class Constraint[T](ABC):
    variables: frozenset[str]

    @classmethod
    def for_vars(cls, *vars: str) -> Self:
        return cls(frozenset(vars))

    @cache
    def is_satisfied(self, state: State[T]) -> bool:
        return self._cached_is_satisfied_with_partial(
            frozenset(
                {
                    (name, var.value)
                    for name, var in state.items()
                    if name in self.variables and var.value is not None
                }
            )
        )

    @cache
    def _cached_is_satisfied_with_partial(
        self, assignment: frozenset[tuple[str, T]]
    ) -> bool:
        return self.is_satisfied_with_partial(assignment)

    @abstractmethod
    def is_satisfied_with_partial(self, assignment: frozenset[tuple[str, T]]) -> bool:
        """Return True if the constraint is satisfied under a partial assignment."""
