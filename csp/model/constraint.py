from csp.state import State, Variable
from abc import ABC, abstractmethod
from typing import Optional
from collections.abc import Set, Sequence


class Constraint[T](ABC):
    def __init__(self, variables: Set[str]) -> None:
        self._variables = set(variables)

    def variables(self) -> Set[str]:
        return self._variables

    def _vars(self, state: State[T]) -> Sequence[Variable[T]]:
        return [state[var] for var in self._variables]

    def _values(self, state: State[T]) -> Sequence[Optional[T]]:
        return [var.value() for var in self._vars(state)]

    def _assigned_values(self, state: State[T]) -> Sequence[T]:
        return [value for value in self._values(state) if value is not None]

    @abstractmethod
    def is_satisfied(self, state: State[T]) -> bool: ...
