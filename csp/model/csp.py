from csp.model.constraint import Constraint
from csp.state import State
from typing import Iterable
from collections.abc import Sequence, Set
from collections import defaultdict


class CSP[T]:
    def __init__(self, constraints: Iterable[Constraint[T]]) -> None:
        self._constraints = list(constraints)
        self._var_to_constraints: dict[str, list[Constraint[T]]] = defaultdict(list)
        self._neighbors: dict[str, set[str]] = defaultdict(set)

        for constraint in self._constraints:
            for var in constraint.variables():
                if constraint not in self._var_to_constraints[var]:
                    self._var_to_constraints[var].append(constraint)
            for a in constraint.variables():
                for b in constraint.variables():
                    if a != b:
                        self._neighbors[a].add(b)

    def constraints(self) -> Sequence[Constraint[T]]:
        return self._constraints

    def constraints_for(self, var: str) -> Sequence[Constraint[T]]:
        return self._var_to_constraints.get(var, list())

    def constraints_between(self, var1: str, var2: str) -> Sequence[Constraint[T]]:
        return [c for c in self.constraints_for(var1) if var2 in c.variables()]

    def neighbors(self, var: str) -> Set[str]:
        return self._neighbors.get(var, set())

    def is_satisfied(self, state: "State[T]") -> bool:
        return all(constraint.is_satisfied(state) for constraint in self._constraints)

    def is_satisfied_for_constraints_for_var(self, var: str, state: State[T]) -> bool:
        return all(
            constraint.is_satisfied(state) for constraint in self.constraints_for(var)
        )

    def is_satisfied_for_constraints_between(
        self, var1: str, var2: str, state: State[T]
    ) -> bool:
        return all(
            constraint.is_satisfied(state)
            for constraint in self.constraints_between(var1, var2)
        )
