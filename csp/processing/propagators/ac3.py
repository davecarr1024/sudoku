from collections import deque

from csp.processing import Propagator
from csp.model import CSP, Constraint
from csp.state import State


class AC3[T](Propagator[T]):
    def propagate(self, csp: CSP[T], state: State[T]) -> Propagator.Result:
        stats = Propagator.Stats()
        queue = deque[(str)]()

        # Initialize queue with all variable names
        for variable_name in state:
            queue.append(variable_name)

        while queue:
            variable_name = queue.popleft()

            # Get all constraints involving this variable
            constraints = csp.constraints_for(variable_name)
            for constraint in constraints:
                for other_name in constraint.variables:
                    if other_name == variable_name:
                        continue

                    # Attempt revision from each neighbor's perspective
                    if self._revise(csp, state, other_name, constraint, stats):
                        if state[other_name].domain_size() == 0:
                            return Propagator.Result(stats=stats, success=False)
                        queue.append(other_name)

        return Propagator.Result(stats=stats, success=True)

    def _revise(
        self,
        csp: CSP[T],
        state: State[T],
        variable_name: str,
        constraint: Constraint[T],
        stats: Propagator.Stats,
    ) -> bool:
        """
        For a given constraint, remove values from variable's domain
        that cannot be extended to a satisfying assignment given the current domains.
        """
        revised = False
        variable = state[variable_name]

        for value in set(variable.domain):
            # Attempt to satisfy the constraint with variable=value
            assignment = {variable_name: value}
            if not self._can_satisfy(constraint, state, assignment, stats):
                variable.remove_value_from_domain(value)
                stats.domain_prunes += 1
                revised = True

        return revised

    def _can_satisfy(
        self,
        constraint: Constraint[T],
        state: State[T],
        assignment: dict[str, T],
        stats: Propagator.Stats,
    ) -> bool:
        """
        Try to complete `assignment` to satisfy the constraint by assigning values
        to unassigned variables, using backtracking with forward-checking and pruning.
        """
        vars = constraint.variables

        # Optimization: sort unassigned vars by domain size (MRV)
        unassigned = [
            var
            for var in vars
            if var not in assignment and not state[var].is_assigned()
        ]
        unassigned.sort(key=lambda var: state[var].domain_size())

        # Early exit: if any variable has no domain left, can't succeed
        if any(state[var].domain_size() == 0 for var in unassigned):
            return False

        assigned_values = set(assignment.get(var) for var in vars if var in assignment)

        def backtrack(index: int) -> bool:
            if index == len(unassigned):
                stats.constraint_checks += 1
                return constraint.is_satisfied_with_partial(assignment)

            var = unassigned[index]
            domain = state[var].domain

            for value in domain:
                if value in assigned_values:
                    continue
                assignment[var] = value
                assigned_values.add(value)

                if backtrack(index + 1):
                    return True

                assigned_values.remove(value)
                del assignment[var]

            return False

        return backtrack(0)
