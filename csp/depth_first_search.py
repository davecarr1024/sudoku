from dataclasses import dataclass
from typing import override, Optional
import time
from functools import lru_cache
from .search_strategy import SearchStrategy
from .state import State
from .solver_stats import SolverStats
from .csp import CSP
from .variable import Variable
from .domain import Domain


@dataclass(frozen=True)
class DepthFirstSearch[T](SearchStrategy[T]):
    minimum_remaining_values: bool = True
    least_constraining_values: bool = True

    @staticmethod
    @lru_cache(maxsize=100_000)
    def _lcv_score(
        value: T,
        variable: Variable[T],
        state: State[T],
        csp: CSP[T],
    ) -> int:
        total_eliminated = 0

        for constraint in csp.constraints_for(variable.name):
            for neighbor_name in constraint.variables:
                if neighbor_name == variable.name:
                    continue
                neighbor = state[neighbor_name]
                if neighbor.is_assigned():
                    continue

                # Simulate assignment
                hypothetical_neighbor = neighbor.with_domain(
                    Domain.for_values(
                        *[
                            v
                            for v in neighbor.domain
                            if constraint.is_satisfied_with_partial(
                                frozenset(
                                    {
                                        (variable.name, value),
                                        (neighbor.name, v),
                                    }
                                )
                            )
                        ]
                    )
                )

                eliminated = len(neighbor.domain) - len(hypothetical_neighbor.domain)
                total_eliminated += eliminated

        return total_eliminated

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
        if self.minimum_remaining_values:
            variable = min(
                (var for var in state.values() if not var.is_assigned()),
                key=lambda var: len(var.domain),
            )
        else:
            variable = next(var for var in state.values() if not var.is_assigned())

        values = variable.domain
        if self.least_constraining_values:
            values = sorted(
                values,
                key=lambda v: DepthFirstSearch[T]._lcv_score(v, variable, state, csp),
            )

        # Try each value in its domain
        for value in values:
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
        stats.elapsed_time = time.perf_counter() - start
        return stats, result
