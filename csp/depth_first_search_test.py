from .depth_first_search import DepthFirstSearch
from .null_propagator import NullPropagator
from .ac3_propagator import AC3Propagator
from .domain import Domain
from .variable import Variable
from .state import State
from .delta_record import DeltaRecord
from .csp import CSP
from .all_different import AllDifferent


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

    solver = DepthFirstSearch(propagator=AC3Propagator())
    result = solver.solve(csp, state)

    assert not result.success


def test_propagation_assists_search():
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
    solver = DepthFirstSearch(propagator=AC3Propagator())
    result = solver.solve(csp, state)

    assert result.success
    assert csp.is_satisfied(state)


def test_mrv_heuristic_effect():
    # A case where MRV will force a variable with fewer options to be chosen first
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1}))
    b = Variable(delta_record, "b", Domain(delta_record, {1, 2, 3}))
    state = State(delta_record, [a, b])
    csp = CSP([AllDifferent({"a", "b"})])

    solver = DepthFirstSearch(propagator=AC3Propagator(), minimum_remaining_values=True)
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
        propagator=AC3Propagator(),
        minimum_remaining_values=True,
        least_constraining_values=True,
    )
    result = solver.solve(csp, state)

    assert result.success
    assert a.value() != b.value()
