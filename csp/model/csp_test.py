from csp.model import CSP
from csp.model.constraints import AllDifferent
from csp.delta import DeltaRecord
from csp.state import State, Variable, Domain
import pytest


@pytest.fixture
def simple_csp_and_state():
    delta = DeltaRecord()
    variables = {
        name: Variable(delta, name, Domain(delta, {1, 2, 3}))
        for name in ["A", "B", "C"]
    }
    state = State(delta, list(variables.values()))
    constraint = AllDifferent({"A", "B", "C"})
    csp = CSP[int]([constraint])
    return csp, state


def test_constraints(simple_csp_and_state):
    csp, _ = simple_csp_and_state
    assert len(csp.constraints()) == 1
    assert isinstance(csp.constraints()[0], AllDifferent)


def test_constraints_for(simple_csp_and_state):
    csp, _ = simple_csp_and_state
    constraints = csp.constraints_for("A")
    assert len(constraints) == 1
    assert isinstance(constraints[0], AllDifferent)


def test_constraints_for_unknown_var(simple_csp_and_state):
    csp, _ = simple_csp_and_state
    assert csp.constraints_for("D") == []


def test_constraints_between(simple_csp_and_state):
    csp, _ = simple_csp_and_state
    between = csp.constraints_between("A", "B")
    assert len(between) == 1
    assert isinstance(between[0], AllDifferent)
    assert csp.constraints_between("A", "Z") == []


def test_neighbors(simple_csp_and_state):
    csp, _ = simple_csp_and_state
    neighbors = csp.neighbors("A")
    assert neighbors == {"B", "C"}


def test_is_satisfied_true(simple_csp_and_state):
    csp, state = simple_csp_and_state
    state["A"].assign(1)
    state["B"].assign(2)
    state["C"].assign(3)
    assert csp.is_satisfied(state)


def test_is_satisfied_false(simple_csp_and_state):
    csp, state = simple_csp_and_state
    state["A"].assign(1)
    state["B"].assign(2)
    state["C"].assign(1)
    assert not csp.is_satisfied(state)


def test_is_satisfied_for_constraints_true(simple_csp_and_state):
    csp, state = simple_csp_and_state
    state["A"].assign(1)
    state["B"].assign(2)
    state["C"].assign(3)
    assert csp.is_satisfied_for_constraints(state, csp.constraints())


def test_is_satisfied_for_constraints_false(simple_csp_and_state):
    csp, state = simple_csp_and_state
    state["A"].assign(2)
    state["B"].assign(2)
    state["C"].assign(3)
    assert not csp.is_satisfied_for_constraints(state, csp.constraints())


def test_is_satisfied_for_constraints_for_var(simple_csp_and_state):
    csp, state = simple_csp_and_state
    state["A"].assign(1)
    state["B"].assign(2)
    state["C"].assign(1)
    assert not csp.is_satisfied_for_constraints_for_var("C", state)


def test_is_satisfied_for_constraints_between(simple_csp_and_state):
    csp, state = simple_csp_and_state
    state["A"].assign(1)
    state["B"].assign(1)
    assert not csp.is_satisfied_for_constraints_between("A", "B", state)
    state["B"].assign(2)
    assert csp.is_satisfied_for_constraints_between("A", "B", state)
