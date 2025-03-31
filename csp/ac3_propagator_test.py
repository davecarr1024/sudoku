from .ac3_propagator import AC3Propagator
from .state import State
from .variable import Variable
from .domain import Domain
from .delta_record import DeltaRecord
from .all_different import AllDifferent
from .csp import CSP


def test_ac3_propagates():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1, 2}))
    b = Variable(delta_record, "b", Domain(delta_record, {2}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])
    result = AC3Propagator().propagate(csp, state)
    assert result.success
    assert a.domain == {1}
    assert b.domain == {2}


def test_ac3_propagation_failure():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {2}))
    b = Variable(delta_record, "b", Domain(delta_record, {2}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])
    result = AC3Propagator().propagate(csp, state)
    assert not result.success


def test_ac3_idempotent():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1}))
    b = Variable(delta_record, "b", Domain(delta_record, {2}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])
    result = AC3Propagator().propagate(csp, state)
    assert result.success
    assert a.domain == {1}
    assert b.domain == {2}
    assert result.stats.domain_prunes == 0


def test_ac3_chain_propagation():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1, 2}))
    b = Variable(delta_record, "b", Domain(delta_record, {2}))
    c = Variable(delta_record, "c", Domain(delta_record, {1, 2}))
    state = State(delta_record, [a, b, c])
    csp = CSP(
        [
            AllDifferent({"a", "b"}),
            AllDifferent({"b", "c"}),
        ]
    )
    result = AC3Propagator().propagate(csp, state)
    assert result.success
    assert a.domain == {1}
    assert b.domain == {2}
    assert c.domain == {1}


def test_ac3_early_failure():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1}))
    b = Variable(delta_record, "b", Domain(delta_record, {1}))
    c = Variable(delta_record, "c", Domain(delta_record, {1}))
    state = State(delta_record, [a, b, c])
    csp = CSP([AllDifferent({"a", "b", "c"})])
    result = AC3Propagator().propagate(csp, state)
    assert not result.success


def test_ac3_prunes_only_if_no_valid_neighbor_values():
    # Setup: a and b are constrained to be different
    # a has {1, 2}, b has {1, 2}
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1, 2}))
    b = Variable(delta_record, "b", Domain(delta_record, {1, 2}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])

    result = AC3Propagator().propagate(csp, state)
    assert result.success
    assert a.domain == {1, 2}
    assert b.domain == {1, 2}

    # Now restrict b's domain to {2}
    b.remove_value_from_domain(1)

    result = AC3Propagator().propagate(csp, state)
    assert result.success
    assert a.domain == {1}  # 2 should be pruned (2 ≠ 2 fails)
    assert b.domain == {2}
