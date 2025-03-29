from .constraint import Constraint
from .state import State
from typing import Iterable, Iterator, override
from collections.abc import Collection


class CSP[T](Collection[Constraint[T]]):
    def __init__(self, constraints: Collection[Constraint[T]]) -> None:
        self._constraints = constraints
        self._by_variable: dict[str, list[Constraint[T]]] = {}
        for constraint in self._constraints:
            for var in constraint.variables:
                self._by_variable.setdefault(var, []).append(constraint)

    @override
    def __len__(self) -> int:
        return len(self._constraints)

    @override
    def __iter__(self) -> Iterator[Constraint[T]]:
        return iter(self._constraints)

    @override
    def __contains__(self, constraint: object) -> bool:
        return constraint in self._constraints

    def constraints(self) -> Iterable[Constraint[T]]:
        return self._constraints

    def constraints_for(self, variable_name: str) -> Iterable[Constraint[T]]:
        return self._by_variable.get(variable_name, [])

    def is_satisfied(self, state: State[T]) -> bool:
        return all(constraint.is_satisfied(state) for constraint in self._constraints)
