from .csp import CSP
from .state import State
from .propagator import Propagator
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class SearchStrategy[T](ABC):
    @dataclass
    class Stats:
        state_visits: int = 0
        assignments: int = 0
        propagations: int = 0
        propagator_stats: Propagator.Stats = field(default_factory=Propagator.Stats)

        def __add__(self, rhs: "SearchStrategy.Stats") -> "SearchStrategy.Stats":
            return SearchStrategy.Stats(
                state_visits=self.state_visits + rhs.state_visits,
                assignments=self.assignments + rhs.assignments,
                propagations=self.propagations + rhs.propagations,
                propagator_stats=self.propagator_stats + rhs.propagator_stats,
            )

    @dataclass
    class Result:
        stats: "SearchStrategy.Stats" = field(
            default_factory=lambda: SearchStrategy.Stats()
        )
        success: bool = True

    @abstractmethod
    def solve(self, csp: CSP[T], state: State[T]) -> "SearchStrategy.Result": ...
