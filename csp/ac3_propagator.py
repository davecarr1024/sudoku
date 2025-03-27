from dataclasses import dataclass
from .constraint_propagator import ConstraintPropagator
from .state import State
from .variable import Variable
from .constraint import Constraint
from .csp import CSP


@dataclass(frozen=True)
class AC3Propagator[T](ConstraintPropagator[T]):
    """
    A constraint propagator that implements a basic version of the AC-3 algorithm.

    This propagator enforces arc consistency by iteratively checking constraints
    between pairs of variables. For each variable, it examines its neighbors under
    each constraint and removes domain values that are no longer consistent.

    Propagation continues until no more domain reductions are possible or a variable's
    domain becomes empty (in which case, propagation fails and returns None).

    This implementation is general-purpose and works with arbitrary constraints that
    implement the `Constraint[T]` protocol.

    Example use:
        propagator = AC3Propagator()
        pruned_state = propagator.propagate(csp, initial_state)

    Returns:
        A new State[T] with possibly reduced domains, or None if a contradiction is found.
    """

    def propagate(self, csp: CSP[T], state: State[T]) -> State[T] | None:
        queue = list(state)

        while queue:
            var_name = queue.pop()
            var = state[var_name]

            for constraint in csp.constraints_for(var_name):
                for neighbor_name in constraint.variables:
                    if neighbor_name == var_name:
                        continue
                    neighbor = state[neighbor_name]
                    revised, new_neighbor = self.revise(
                        var, neighbor, constraint, state
                    )
                    if revised:
                        if not new_neighbor.is_valid():
                            return None
                        state = state.with_variable(new_neighbor)
                        if neighbor_name not in queue:
                            queue.append(neighbor_name)

        return state

    def revise(
        self,
        var: Variable[T],
        neighbor: Variable[T],
        constraint: Constraint[T],
        state: State[T],
    ) -> tuple[bool, Variable[T]]:
        """
        Attempts to prune the domain of `neighbor` based on the given constraint and
        the current value/domain of `var`.

        For each value in `neighbor`'s domain, this method simulates assigning that
        value and checks if the constraint would still be satisfied. If not, the value
        is removed from the domain.

        Returns:
            - A boolean indicating whether the domain was changed
            - The updated Variable[T] with a potentially smaller domain
        """
        revised = False
        new_domain = neighbor.domain

        for value in neighbor.domain:
            test_neighbor = neighbor.assign(value)
            test_state = state.with_variable(test_neighbor)

            if not constraint.is_satisfied(test_state):
                new_domain = new_domain.without_value(value)
                revised = True

        if neighbor.value is not None and neighbor.value not in new_domain:
            return False, None  # contradiction
        return revised, neighbor.with_domain(new_domain)
