from csp.model import Constraint
from csp.state import State
from typing import override


class AllDifferent[T](Constraint[T]):
    @override
    def is_satisfied(self, state: State[T]) -> bool:
        values = self._assigned_values(state)
        return len(values) == len(set(values))
