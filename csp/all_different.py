from .constraint import Constraint
from typing import Mapping, override


class AllDifferent[T](Constraint[T]):
    @override
    def is_satisfied_with_partial(self, assignment: Mapping[str, T]) -> bool:
        return len(assignment) == len(set(assignment.values()))
