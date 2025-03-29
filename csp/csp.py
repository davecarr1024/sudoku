from dataclasses import dataclass
from typing import Iterable, Iterator, Sized, override
from functools import cache
from .constraint import Constraint
from .state import State


@dataclass(frozen=True)
class CSP[T](Sized, Iterable[Constraint[T]]):
    constraints: frozenset[Constraint[T]]

    @classmethod
    def for_constraints(cls, *constraints: Constraint[T]) -> "CSP[T]":
        return cls(frozenset(constraints))

    @override
    def __len__(self) -> int:
        return len(self.constraints)

    @override
    def __iter__(self) -> Iterator[Constraint[T]]:
        return iter(self.constraints)

    @cache
    def constraints_for(self, variable: str) -> Iterable[Constraint[T]]:
        return tuple(
            constraint
            for constraint in self.constraints
            if variable in constraint.variables
        )

    def is_satisfied(self, state: State[T]) -> bool:
        return all(constraint.is_satisfied(state) for constraint in self)
