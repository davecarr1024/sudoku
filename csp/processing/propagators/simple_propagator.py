from csp.processing import Propagator
from csp.model import CSP
from csp.state import State
from typing import override


class SimplePropagator[T](Propagator[T]):
    @override
    def propagate(self, csp: CSP[T], state: State[T]) -> Propagator.Result:
        stats = Propagator.Stats()
        for variable in state.variables():
            if variable.is_assigned():
                continue
            for value in variable.domain_values():
                with variable.maintain_state():
                    variable.assign(value)
                    constraints = csp.constraints_for(variable.name)
                    stats.constraint_checks += len(constraints)
                    if csp.is_satisfied_for_constraints(state, constraints):
                        continue
                variable.remove_value_from_domain(value)
                stats.domain_prunes += 1
            if variable.domain_size() == 0:
                return Propagator.Result(success=False, stats=stats)
        return Propagator.Result(success=True, stats=stats)
