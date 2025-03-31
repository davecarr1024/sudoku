from csp.model.constraint import Constraint
from csp.state import State
from typing import Iterable, Iterator, override
from collections.abc import Set
from collections import defaultdict


class CSP[T](Set[Constraint[T]]):
    def __init__(self, constraints: Iterable[Constraint[T]]) -> None:
        self._constraints = set(constraints)
        self._var_to_constraints: dict[str, set[Constraint[T]]] = defaultdict(set)
        self._neighbors: dict[str, set[str]] = defaultdict(set)

        for constraint in self._constraints:
            for var in constraint.variables:
                self._var_to_constraints[var].add(constraint)
            for a in constraint.variables:
                for b in constraint.variables:
                    if a != b:
                        self._neighbors[a].add(b)

    @override
    def __iter__(self) -> Iterator[Constraint[T]]:
        return iter(self._constraints)

    @override
    def __contains__(self, item: object) -> bool:
        return item in self._constraints

    @override
    def __len__(self) -> int:
        return len(self._constraints)

    def constraints(self) -> set[Constraint[T]]:
        return self._constraints

    def constraints_for(self, var: str) -> set[Constraint[T]]:
        return self._var_to_constraints.get(var, set())

    def constraints_between(self, var1: str, var2: str) -> set[Constraint[T]]:
        return {
            c for c in self._var_to_constraints.get(var1, set()) if var2 in c.variables
        }

    def neighbors(self, var: str) -> set[str]:
        return self._neighbors.get(var, set())

    def is_satisfied(self, state: "State[T]") -> bool:
        return all(constraint.is_satisfied(state) for constraint in self._constraints)
