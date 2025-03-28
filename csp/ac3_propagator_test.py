from .ac3_propagator import AC3Propagator
from .state import State
from .csp import CSP
from .variable import Variable
from .domain import Domain
from .all_different_constraint import AllDifferentConstraint


def test_propagates_all_different_removes_assigned_value():
    # A and B must be different
    csp = CSP([AllDifferentConstraint.for_vars("A", "B")])

    state = (
        State()
        .with_variable(Variable.make("A", 1, 2, 3, assigned=1))
        .with_variable(Variable.make("B", 1, 2, 3))
    )

    result = AC3Propagator().propagate(csp, state)
    assert result is not None
    assert result["B"].domain == Domain.for_values(2, 3)


def test_propagation_failure_due_to_empty_domain():
    # A and B must be different, but B only has 1
    csp = CSP([AllDifferentConstraint.for_vars("A", "B")])

    state = (
        State()
        .with_variable(Variable.make("A", 1, assigned=1))
        .with_variable(Variable.make("B", 1))
    )

    result = AC3Propagator().propagate(csp, state)
    assert result is None


def test_no_domain_change_when_constraint_already_satisfied():
    # A and B already assigned different values
    csp = CSP([AllDifferentConstraint.for_vars("A", "B")])

    state = (
        State()
        .with_variable(Variable.make("A", 1, assigned=1))
        .with_variable(Variable.make("B", 2, 3, assigned=2))
    )

    result = AC3Propagator().propagate(csp, state)
    assert result == state  # no change expected
