from csp.processing import Propagator
from csp.model import CSP
from csp.state import State, Variable
from typing import override


class AC3[T](Propagator[T]):
    @override
    def propagate(self, csp: CSP[T], state: State[T]) -> Propagator.Result:
        stats = Propagator.Stats()
        queue = set[tuple[str, str]]()
        for var1 in state.variables():
            for constraint in csp.constraints_for(var1.name):
                for var2_name in constraint.variables():
                    queue.add((var1.name, var2_name))

        def is_supported(var: Variable[T], value: T, neighbor: Variable[T]) -> bool:
            neighbor_value = neighbor.value()
            neighbor_values: set[T] = (
                neighbor.domain_values() if neighbor_value is None else {neighbor_value}
            )

            with var.maintain_state():
                var.assign(value)
                with neighbor.maintain_state():
                    for y in neighbor_values:
                        neighbor.assign(y)
                        stats.constraint_checks += 1
                        if csp.is_satisfied_for_constraints_between(
                            var.name,
                            neighbor.name,
                            state,
                        ):
                            return True
            return False

        while queue:
            var_name, neighbor_name = queue.pop()
            var = state[var_name]
            neighbor = state[neighbor_name]

            if var.is_assigned():
                continue

            for value in list(var.domain_values()):
                if not is_supported(var, value, neighbor):
                    var.remove_value_from_domain(value)
                    stats.domain_prunes += 1
                    if var.domain_size() == 0:
                        return Propagator.Result(success=False, stats=stats)
                    for new_var in csp.neighbors(var.name):
                        queue.add((new_var, var.name))

        return Propagator.Result(success=True, stats=stats)
