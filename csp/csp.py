from dataclasses import dataclass
from typing import Iterable, Iterator, Sized, Sequence, override
from .constraint import Constraint
from .state import State


@dataclass(frozen=True)
class CSP[T](Sized, Iterable[Constraint[T]]):
    constraints: Sequence[Constraint[T]]

    @override
    def __len__(self) -> int:
        return len(self.constraints)

    @override
    def __iter__(self) -> Iterator[Constraint[T]]:
        return iter(self.constraints)

    def constraints_for(self, variable: str) -> Iterable[Constraint[T]]:
        return filter(lambda constraint: variable in constraint.variables, self)

    def is_satisfied(self, state: State[T]) -> bool:
        return all(constraint.is_satisfied(state) for constraint in self)
