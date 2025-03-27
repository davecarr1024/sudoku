from .constraint import Constraint
from .state import State
from dataclasses import dataclass
from typing import override


@dataclass(frozen=True)
class AllDifferentConstraint[T](Constraint[T]):
    @override
    def is_satisfied(self, state: State[T]) -> bool:
        values = [
            variable.value
            for name, variable in state.items()
            if name in self.variables and variable.is_assigned()
        ]
        return len(values) == len(set(values))
