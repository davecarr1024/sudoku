from .state import State
from .variable import Variable
from .domain import Domain


def test_with_variable():
    assert State().with_variable(Variable("a", Domain.for_values(1, 2, 3))) == State(
        {
            "a": Variable("a", Domain.for_values(1, 2, 3)),
        }
    )


def test_is_valid(subtests):
    for state, expected in list[tuple[State, bool]](
        [
            (
                State(),
                True,
            ),
            (
                State().with_variable(Variable("a", Domain.for_values(1, 2, 3))),
                True,
            ),
            (
                State().with_variable(Variable("a", Domain())),
                False,
            ),
        ]
    ):
        with subtests.test(state=state, expected=expected):
            assert state.is_valid() == expected


def test_unassigned_variables(subtests):
    for state, expected in list[tuple[State, list[Variable]]](
        [
            (
                State(),
                [],
            ),
            (
                State().with_variable(Variable("a", Domain.for_values(1, 2, 3))),
                [Variable("a", Domain.for_values(1, 2, 3))],
            ),
            (
                State().with_variable(Variable("a", Domain.for_values(1, 2, 3), 1)),
                [],
            ),
        ]
    ):
        with subtests.test(state=state, expected=expected):
            assert list(state.unassigned_variables()) == expected


def test_assign():
    assert State().with_variable(Variable("a", Domain.for_values(1, 2, 3))).assign(
        "a", 1
    ) == State().with_variable(Variable("a", Domain.for_values(1), 1))
