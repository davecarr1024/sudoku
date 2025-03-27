from dataclasses import dataclass
from typing import override, Optional
import time
from .search_strategy import SearchStrategy
from .state import State
from .solver_stats import SolverStats
from .csp import CSP


@dataclass(frozen=True)
class DepthFirstSearch[T](SearchStrategy[T]):
    use_minimum_remaining_values: bool = True

    def _solve(
        self, csp: CSP[T], state: State[T], depth: int
    ) -> tuple[SolverStats, Optional[State[T]]]:
        stats = SolverStats(max_depth=depth, state_visits=1)

        # Fail fast if the state is invalid
        if not state.is_valid():
            return stats, None

        # Success condition: all variables are assigned
        if all(var.is_assigned() for var in state.values()):
            return stats, state

        # Choose the next unassigned variable (leftmost strategy)
        if self.use_minimum_remaining_values:
            variable = min(
                (var for var in state.values() if not var.is_assigned()),
                key=lambda var: len(var.domain),
            )
        else:
            variable = next(var for var in state.values() if not var.is_assigned())

        # Try each value in its domain
        for value in variable.domain:
            stats.assignments += 1
            assigned = variable.assign(value)
            next_state = state.with_variable(assigned)

            # Propagate constraints after the assignment
            stats.propagations += 1
            propagated = self.propagator.propagate(csp, next_state)
            if propagated is None:
                continue  # failed propagation — backtrack

            child_stats, result = self._solve(csp, propagated, depth + 1)
            stats = stats.merge(child_stats)
            if result is not None:
                return stats, result  # found a solution

        # All values failed — backtrack
        return stats, None

    @override
    def solve(
        self, csp: CSP[T], state: State[T]
    ) -> tuple[SolverStats, Optional[State[T]]]:
        start = time.perf_counter()
        stats, result = self._solve(csp, state, 0)
        stats.elapsed_seconds = time.perf_counter() - start
        return stats, result
