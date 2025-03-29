from .all_different import AllDifferent
from .state import State
from .variable import Variable
from .delta_record import DeltaRecord
from .domain import Domain


def test_is_satisfied_with_partial():
    assert AllDifferent[int]({"a", "b"}).is_satisfied_with_partial({"a": 1, "b": 2})
    assert not AllDifferent[int]({"a", "b"}).is_satisfied_with_partial({"a": 1, "b": 1})


def test_is_satisfied():
    delta_record = DeltaRecord()
    assert AllDifferent[int]({"a", "b"}).is_satisfied(
        State(
            delta_record,
            [
                Variable(delta_record, "a", Domain(delta_record, {1, 2}), 1),
                Variable(delta_record, "b", Domain(delta_record, {1, 2}), 2),
            ],
        )
    )
    assert not AllDifferent[int]({"a", "b"}).is_satisfied(
        State(
            delta_record,
            [
                Variable(delta_record, "a", Domain(delta_record, {1, 2}), 1),
                Variable(delta_record, "b", Domain(delta_record, {1, 2}), 1),
            ],
        )
    )


def test_is_satisfied_with_unassigned():
    delta_record = DeltaRecord()
    state = State(
        delta_record,
        [
            Variable(delta_record, "a", Domain(delta_record, {1, 2}), 1),
            Variable(delta_record, "b", Domain(delta_record, {1, 2})),  # unassigned
        ],
    )
    assert AllDifferent[int]({"a", "b"}).is_satisfied(state)
