from dataclasses import dataclass
from typing import override
from .constraint import Constraint


@dataclass(frozen=True)
class AllDifferentConstraint[T](Constraint[T]):
    @override
    def is_satisfied_with_partial(self, assignment: frozenset[tuple[str, T]]) -> bool:
        return len(assignment) == len({v for _, v in assignment})
