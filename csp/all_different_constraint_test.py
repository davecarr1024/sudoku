from .state import State
from .all_different_constraint import AllDifferentConstraint
from .variable import Variable


def test_is_satisfied(subtests):
    for constraint, state, expected in list[tuple[AllDifferentConstraint, State, bool]](
        [
            (
                AllDifferentConstraint.for_vars("a", "b", "c"),
                State(),
                True,
            ),
            (
                AllDifferentConstraint.for_vars("a", "b", "c"),
                State()
                .with_variable(Variable.make("a", 1, assigned=1))
                .with_variable(Variable.make("b", 2, assigned=2)),
                True,
            ),
            (
                AllDifferentConstraint.for_vars("a", "b", "c"),
                State()
                .with_variable(Variable.make("a", 1, assigned=1))
                .with_variable(Variable.make("b", 1, assigned=1)),
                False,
            ),
        ]
    ):
        with subtests.test(constraint=constraint, state=state, expected=expected):
            assert constraint.is_satisfied(state) == expected


def test_is_satisfied_with_partial(subtests):
    for constraint, assignment, expected in list[
        tuple[AllDifferentConstraint, frozenset[tuple[str, int]], bool]
    ](
        [
            (
                AllDifferentConstraint.for_vars("a", "b", "c"),
                frozenset(
                    {
                        ("a", 1),
                        ("b", 2),
                    }
                ),
                True,
            ),
            (
                AllDifferentConstraint.for_vars("a", "b", "c"),
                frozenset(
                    {
                        ("a", 1),
                        ("b", 1),
                    }
                ),
                False,
            ),
        ]
    ):
        with subtests.test(
            constraint=constraint, assignment=assignment, expected=expected
        ):
            assert constraint.is_satisfied_with_partial(assignment) == expected
