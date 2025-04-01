from csp.model.constraints import AllDifferent
from csp.state import State, Variable, Domain
from csp.delta import DeltaRecord


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
