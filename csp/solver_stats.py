from dataclasses import dataclass, replace
from typing import Self


@dataclass
class SolverStats:
    state_visits: int = 0
    assignments: int = 0
    propagations: int = 0
    max_depth: int = 0
    elapsed_time: float = 0

    def merge(self, rhs: Self) -> Self:
        return replace(
            self,
            state_visits=self.state_visits + rhs.state_visits,
            assignments=self.assignments + rhs.assignments,
            propagations=self.propagations + rhs.propagations,
            max_depth=max(self.max_depth, rhs.max_depth),
        )
