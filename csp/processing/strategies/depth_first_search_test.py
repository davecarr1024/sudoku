from csp.processing.strategies import DepthFirstSearch
from csp.processing.propagators import NullPropagator
from csp.state import Domain, Variable, State
from csp.delta import DeltaRecord
from csp.model import CSP
from csp.model.constraints import AllDifferent


def test_basic_solution():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1, 2}))
    b = Variable(delta_record, "b", Domain(delta_record, {1, 2}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])

    solver = DepthFirstSearch(propagator=NullPropagator())
    result = solver.solve(csp, state)

    assert result.success
    values = {var.name: var.value() for var in state.variables()}
    assert values["a"] != values["b"]
    assert {values["a"], values["b"]} == {1, 2}


def test_unsolvable():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1}))
    b = Variable(delta_record, "b", Domain(delta_record, {1}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])

    solver = DepthFirstSearch(NullPropagator())
    result = solver.solve(csp, state)

    assert not result.success


def test_mrv_heuristic_effect():
    # A case where MRV will force a variable with fewer options to be chosen first
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1}))
    b = Variable(delta_record, "b", Domain(delta_record, {1, 2, 3}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])

    solver = DepthFirstSearch(
        propagator=NullPropagator(), minimum_remaining_values=True
    )
    result = solver.solve(csp, state)

    assert result.success
    assert a.value() == 1
    assert b.value() != 1


def test_lcv_heuristic_does_not_break_correctness():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1, 2}))
    b = Variable(delta_record, "b", Domain(delta_record, {1, 2}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])

    solver = DepthFirstSearch(
        propagator=NullPropagator(),
        minimum_remaining_values=True,
        least_constraining_values=True,
    )
    result = solver.solve(csp, state)

    assert result.success
    assert a.value() != b.value()
