from .state import State
from .all_different_constraint import AllDifferentConstraint
from .variable import Variable
from .domain import Domain


def test_is_satisfied(subtests):
    for constraint, state, expected in list[tuple[AllDifferentConstraint, State, bool]](
        [
            (
                AllDifferentConstraint(variables={"a", "b", "c"}),
                State(),
                True,
            ),
            (
                AllDifferentConstraint(variables={"a", "b", "c"}),
                State(
                    {
                        "a": Variable("a", Domain.for_values(1), 1),
                        "b": Variable("b", Domain.for_values(2), 2),
                    }
                ),
                True,
            ),
            (
                AllDifferentConstraint(variables={"a", "b", "c"}),
                State(
                    {
                        "a": Variable("a", Domain.for_values(1), 1),
                        "b": Variable("b", Domain.for_values(1), 1),
                    }
                ),
                False,
            ),
        ]
    ):
        with subtests.test(constraint=constraint, state=state, expected=expected):
            assert constraint.is_satisfied(state) == expected
