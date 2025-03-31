from csp.processing import Propagator
from csp.model import CSP, Constraint
from csp.state import State, Variable
from collections import deque
from collections.abc import Mapping


class AC3[T](Propagator[T]):
    def propagate(self, csp: CSP[T], state: State[T]) -> Propagator.Result:
        """
        Applies the AC-3 (Arc Consistency 3) algorithm to enforce arc consistency on the CSP.

        Iteratively removes inconsistent values from variable domains by checking binary
        constraints between each variable and its neighbors. If any domain becomes empty,
        propagation fails and returns success=False.

        Args:
            csp: The CSP instance containing constraints.
            state: The current state of variable assignments and domains.

        Returns:
            Propagator.Result indicating success or failure, along with propagation stats.
        """
        stats = Propagator.Stats()
        queue = deque[tuple[str, str]]()

        # Initialize queue with all directed arcs (variable, neighbor)
        for constraint in csp:
            for variable_name in constraint.variables:
                for neighbor_name in constraint.variables:
                    if variable_name != neighbor_name:
                        queue.append((variable_name, neighbor_name))

        in_queue = set(queue)

        while queue:
            variable_name, neighbor_name = queue.popleft()
            in_queue.remove((variable_name, neighbor_name))
            variable = state[variable_name]
            neighbor = state[neighbor_name]

            if self._revise(csp, state, variable, neighbor, stats):
                if variable.domain_size() == 0:
                    return Propagator.Result(stats=stats, success=False)
                for other_neighbor_name in csp.neighbors(variable.name):
                    if (
                        other_neighbor_name != neighbor.name
                        and (other_neighbor_name, variable.name) not in in_queue
                    ):
                        queue.append((other_neighbor_name, variable.name))
                        in_queue.add((other_neighbor_name, variable.name))

        return Propagator.Result(stats=stats, success=True)

    def _revise(
        self,
        csp: CSP[T],
        state: State[T],
        variable: Variable[T],
        neighbor: Variable[T],
        stats: Propagator.Stats,
    ) -> bool:
        """
        Removes values from `variable`'s domain that are inconsistent with `neighbor`'s domain.

        For each value in `variable`'s domain, checks whether there is some value in
        `neighbor`'s domain that satisfies all constraints between them. If no such
        value exists, the value is pruned from `variable`'s domain.

        Args:
            csp: The CSP instance containing constraints.
            state: The current state of variable assignments and domains.
            variable: The variable whose domain is being revised.
            neighbor: The neighbor variable that `variable` is being checked against.
            stats: Statistics object to track constraint checks and domain prunes.

        Returns:
            True if any values were removed from `variable`'s domain, otherwise False.
        """
        revised = False
        constraints = csp.constraints_between(variable.name, neighbor.name)

        def _satisfies_constraint(
            constraint: Constraint[T], assignment: Mapping[str, T]
        ) -> bool:
            stats.constraint_checks += 1
            return constraint.is_satisfied_with_partial(assignment)

        def _satisfies_constraints(assignment: Mapping[str, T]) -> bool:
            return all(
                _satisfies_constraint(constraint, assignment)
                for constraint in constraints
            )

        def _satisfies_constraints_for_neighbor_value(
            value: T, neighbor_value: T
        ) -> bool:
            return _satisfies_constraints(
                {variable.name: value, neighbor.name: neighbor_value}
            )

        def _satisfies_constraints_for_neighbor_values(value: T) -> bool:
            return any(
                _satisfies_constraints_for_neighbor_value(value, neighbor_value)
                for neighbor_value in neighbor.domain
            )

        for value in set(variable.domain):
            if not _satisfies_constraints_for_neighbor_values(value):
                variable.remove_value_from_domain(value)
                stats.domain_prunes += 1
                revised = True

        return revised
