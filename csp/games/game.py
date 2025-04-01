from abc import ABC, abstractmethod
from csp.model import CSP
from csp.state import State
from csp.processing import SearchStrategy
from typing import Self


class Game[T](ABC):
    class Error(Exception): ...

    @abstractmethod
    def to_state(self) -> tuple[CSP[T], State[T]]: ...

    @classmethod
    @abstractmethod
    def from_state(cls, csp: CSP[T], state: State[T]) -> Self: ...

    def solve(self, strategy: SearchStrategy[T]) -> tuple[Self, SearchStrategy.Stats]:
        csp, state = self.to_state()
        result = strategy.solve(csp, state)
        if not result.success:
            raise self.Error("No solution found")
        if not state.is_valid():
            raise self.Error("Solution state is not valid")
        if not csp.is_satisfied(state):
            raise self.Error("CSP is not satisfied")
        return (self.from_state(csp, state), result.stats)
