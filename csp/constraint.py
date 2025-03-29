from .state import State
from abc import ABC, abstractmethod
from typing import Mapping


class Constraint[T](ABC):
    def __init__(self, variables: set[str]) -> None:
        self.variables = variables

    @abstractmethod
    def is_satisfied_with_partial(self, assignment: Mapping[str, T]) -> bool: ...

    def is_satisfied(self, state: State[T]) -> bool:
        return self.is_satisfied_with_partial(
            {
                var: value
                for var, value in ((v, state[v].value()) for v in self.variables)
                if value is not None
            }
        )
