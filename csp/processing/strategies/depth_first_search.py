from csp.model import CSP
from csp.state import State, Variable
from csp.processing import Propagator, SearchStrategy


class DepthFirstSearch[T](SearchStrategy[T]):
    def __init__(
        self,
        propagator: Propagator[T],
        minimum_remaining_values: bool = True,
        least_constraining_values: bool = True,
    ) -> None:
        self._propagator = propagator
        self._mrv = minimum_remaining_values
        self._lcv = least_constraining_values

    def solve(self, csp: CSP[T], state: State[T]) -> SearchStrategy.Result:
        stats = SearchStrategy.Stats()
        result = self._propagator.propagate(csp, state)
        stats.propagations += 1
        stats.propagator_stats += result.stats
        if not result.success:
            return SearchStrategy.Result(success=False, stats=stats)
        success = self._dfs(csp, state, stats, 0)
        return SearchStrategy.Result(success=success, stats=stats)

    def _dfs(
        self,
        csp: CSP[T],
        state: State[T],
        stats: SearchStrategy.Stats,
        depth: int,
    ) -> bool:
        stats.state_visits += 1
        stats.max_depth = max(stats.max_depth, depth)

        # values = {name: var.value() for name, var in state.items() if var.is_assigned()}
        # print(f"dfs: depth = {depth} stats = {stats} values = {values}")

        if not state.is_valid():
            return False

        if not csp.is_satisfied(state):
            return False

        if all(v.is_assigned() for v in state.variables()):
            return True

        # Select unassigned variable
        def variable_key(var: Variable[T]) -> int:
            return var.domain_size() if self._mrv else 0

        variable = min(state.unassigned_variables(), key=variable_key)

        def value_key(value: T) -> int:
            if not self._lcv:
                return 0
            return self._lcv_score(csp, state, variable, value)

        for value in sorted(variable.domain_values(), key=value_key):
            checkpoint = state.checkpoint()
            variable.assign(value)
            stats.assignments += 1

            result = self._propagator.propagate(csp, state)
            stats.propagations += 1
            stats.propagator_stats += result.stats

            if result.success:
                if self._dfs(csp, state, stats, depth + 1):
                    return True  # <- early return preserves solution

            state.revert_to(checkpoint)

        return False

    def _lcv_score(
        self, csp: CSP[T], state: State[T], variable: Variable[T], value: T
    ) -> int:
        # Lower score = more preferred
        score = 0
        for constraint in csp.constraints_for(variable.name):
            for var_name in constraint.variables:
                if var_name == variable.name:
                    continue
                other = state[var_name]
                for other_value in other.domain_values():
                    assignment = {variable.name: value, other.name: other_value}
                    if not constraint.is_satisfied_with_partial(assignment):
                        score += 1
        return score
