import pytest
from csp.processing.propagators.simple_propagator import SimplePropagator
from csp.model import CSP
from csp.model.constraints import AllDifferent
from csp.delta import DeltaRecord
from csp.state import State, Variable, Domain


@pytest.fixture
def small_csp_and_state():
    delta = DeltaRecord()
    variables = {
        name: Variable(delta, name, Domain(delta, {1, 2, 3})) for name in ["A", "B"]
    }
    state = State(delta, list(variables.values()))
    constraint = AllDifferent({"A", "B"})
    csp = CSP[int]([constraint])
    return csp, state


def test_propagate_success(small_csp_and_state):
    csp, state = small_csp_and_state
    state["A"].assign(1)  # Should leave 2 and 3 for B

    propagator = SimplePropagator[int]()
    result = propagator.propagate(csp, state)

    assert result.success is True
    assert state["B"].domain_values() == {2, 3}
    assert result.stats.domain_prunes == 1  # value 1 removed
    assert result.stats.constraint_checks > 0


def test_propagate_failure_due_to_empty_domain(small_csp_and_state):
    csp, state = small_csp_and_state

    # Assign A to 1, and shrink B's domain to just 1 (conflict)
    state["A"].assign(1)
    state["B"].domain.remove_value(2)
    state["B"].domain.remove_value(3)

    propagator = SimplePropagator[int]()
    result = propagator.propagate(csp, state)

    assert result.success is False
    assert result.stats.domain_prunes > 0
