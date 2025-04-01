import pytest
from csp.processing.propagators import AC3
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

    propagator = AC3[int]()
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

    propagator = AC3[int]()
    result = propagator.propagate(csp, state)

    assert result.success is False
    assert result.stats.domain_prunes > 0


def test_ac3_chain_propagation():
    delta = DeltaRecord()
    a = Variable(delta, "A", Domain(delta, {1}), 1)
    b = Variable(delta, "B", Domain(delta, {1, 2}))
    c = Variable(delta, "C", Domain(delta, {1, 2, 3}))
    state = State(delta, [a, b, c])
    csp = CSP[int](
        [
            AllDifferent({"A", "B"}),
            AllDifferent({"B", "C"}),
        ]
    )

    result = AC3[int]().propagate(csp, state)

    assert result.success is True
    assert 1 not in b.domain_values()
    assert 2 not in c.domain_values()


def test_ac3_cascade_failure():
    delta = DeltaRecord()
    a = Variable(delta, "A", Domain(delta, {1}), 1)
    b = Variable(delta, "B", Domain(delta, {1}))
    c = Variable(delta, "C", Domain(delta, {1}))
    state = State(delta, [a, b, c])
    csp = CSP[int](
        [
            AllDifferent({"A", "B"}),
            AllDifferent({"B", "C"}),
        ]
    )

    result = AC3[int]().propagate(csp, state)

    assert result.success is False


def test_ac3_no_prune_when_disjoint():
    delta = DeltaRecord()
    a = Variable(delta, "A", Domain(delta, {1}))
    b = Variable(delta, "B", Domain(delta, {2, 3}))
    state = State(delta, [a, b])
    csp = CSP[int]([AllDifferent({"A", "B"})])

    result = AC3[int]().propagate(csp, state)

    assert result.success is True
    assert b.domain_values() == {2, 3}
    assert result.stats.domain_prunes == 0


def test_ac3_symmetric_prune():
    delta = DeltaRecord()
    a = Variable(delta, "A", Domain(delta, {1, 2}))
    b = Variable(delta, "B", Domain(delta, {1}))
    state = State(delta, [a, b])
    csp = CSP[int]([AllDifferent({"A", "B"})])

    result = AC3[int]().propagate(csp, state)

    assert result.success is True
    assert a.domain_values() == {2}
    assert result.stats.domain_prunes == 1
