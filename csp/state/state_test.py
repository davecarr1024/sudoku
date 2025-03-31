from csp.state.state import State
from csp.state.variable import Variable
from csp.state.domain import Domain
from csp.delta import DeltaRecord
import pytest


def test_mapping():
    delta_record = DeltaRecord()
    state = State(
        delta_record,
        [
            Variable(delta_record, "a", Domain(delta_record, {1, 2, 3})),
            Variable(delta_record, "b", Domain(delta_record, {4, 5, 6})),
            Variable(delta_record, "c", Domain(delta_record, {7, 8, 9})),
        ],
    )
    assert set(state.keys()) == {"a", "b", "c"}
    assert {v.name for v in state.variables()} == {"a", "b", "c"}
    assert state["a"].domain == {1, 2, 3}
    with pytest.raises(State.KeyError):
        state["d"]


def test_invalid_delta_record():
    delta_record = DeltaRecord()
    with pytest.raises(State.Error):
        State(DeltaRecord(), [Variable(delta_record, "a", Domain(delta_record, {1}))])


def test_assign():
    delta_record = DeltaRecord()
    state = State(
        delta_record, [Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))]
    )
    assert state["a"].value() is None
    assert not state["a"].is_assigned()
    state.assign("a", 2)
    assert state["a"].value() == 2
    assert state["a"].is_assigned()
    state.revert()
    assert state["a"].value() is None
    assert not state["a"].is_assigned()


def test_unassign():
    delta_record = DeltaRecord()
    state = State(
        delta_record, [Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))]
    )
    assert state["a"].value() is None
    assert not state["a"].is_assigned()
    state.assign("a", 2)
    assert state["a"].value() == 2
    assert state["a"].is_assigned()
    state.unassign("a")
    assert state["a"].value() is None
    assert not state["a"].is_assigned()
    state.revert()
    assert state["a"].value() == 2
    assert state["a"].is_assigned()
    state.revert()
    assert state["a"].value() is None
    assert not state["a"].is_assigned()


def test_maintain_state():
    delta_record = DeltaRecord()
    state = State(
        delta_record, [Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))]
    )
    assert state["a"].value() is None
    with state.maintain_state():
        state.assign("a", 1)
        assert state["a"].value() == 1
    assert state["a"].value() is None


def test_redundant_assignment():
    delta_record = DeltaRecord()
    state = State(
        delta_record, [Variable(delta_record, "a", Domain(delta_record, {1, 2}))]
    )
    state.assign("a", 1)
    state.assign("a", 1)
    state.revert()
    assert state["a"].value() == 1  # Should still be 1
    state.revert()
    assert state["a"].value() is None


def test_revert_underflow():
    delta_record = DeltaRecord()
    state = State(
        delta_record, [Variable(delta_record, "a", Domain(delta_record, {1}))]
    )
    with pytest.raises(DeltaRecord.Error):
        state.revert()


def test_unassigned_variables():
    delta_record = DeltaRecord()
    state = State(
        delta_record,
        [
            Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}), 1),
            Variable(delta_record, "b", Domain(delta_record, {4, 5, 6})),
            Variable(delta_record, "c", Domain(delta_record, {7, 8, 9})),
        ],
    )
    assert set(var.name for var in state.variables()) == {"a", "b", "c"}
    assert set(var.name for var in state.unassigned_variables()) == {"b", "c"}


def test_is_valid():
    delta_record = DeltaRecord()
    assert State(
        delta_record,
        [
            Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}), 1),
            Variable(delta_record, "b", Domain(delta_record, {4, 5, 6})),
            Variable(delta_record, "c", Domain(delta_record, {7, 8, 9})),
        ],
    ).is_valid()
    assert not State(
        delta_record,
        [
            Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}), 1),
            Variable(delta_record, "b", Domain(delta_record, {4, 5, 6})),
            Variable(delta_record, "c", Domain(delta_record, set())),
        ],
    ).is_valid()


def test_nested_maintain_state():
    delta_record = DeltaRecord()
    state = State(
        delta_record, [Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))]
    )

    assert state["a"].value() is None

    with state.maintain_state():
        state.assign("a", 1)
        assert state["a"].value() == 1

        with state.maintain_state():
            state.assign("a", 2)
            assert state["a"].value() == 2
        # Inner context reverted
        assert state["a"].value() == 1

    # Outer context reverted
    assert state["a"].value() is None
