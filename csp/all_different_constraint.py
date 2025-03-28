from dataclasses import dataclass
from typing import override
from collections.abc import Mapping, Collection
from functools import cache
from .constraint import Constraint


@dataclass(frozen=True)
class AllDifferentConstraint[T](Constraint[T]):
    @cache
    @staticmethod
    def _is_satisfied_with_partial(items: Collection[tuple[str, T]]) -> bool:
        return len(items) == len(set(v for _, v in items))

    @override
    def is_satisfied_with_partial(self, assignment: Mapping[str, T]) -> bool:
        return AllDifferentConstraint[T]._is_satisfied_with_partial(
            tuple(sorted(assignment.items()))
        )
