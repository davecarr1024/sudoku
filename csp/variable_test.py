from .variable import Variable
from .domain import Domain
from .delta_record import DeltaRecord
import pytest


def test_assign_value():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))
    assert variable.name == "a"
    assert variable.value() is None
    assert variable.domain == {1, 2, 3}
    assert not variable.is_assigned()
    assert variable.value() is None
    variable.assign(1)
    assert variable.value() == 1
    assert variable.is_assigned()
    variable.revert()
    assert variable.value() is None
    assert not variable.is_assigned()


def test_build_with_invalid_value():
    delta_record = DeltaRecord()
    with pytest.raises(Variable.ValueError):
        Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}), 4)


def test_assign_invalid_value():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))
    with pytest.raises(Variable.ValueError):
        variable.assign(4)


def test_unassign_value():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}), 1)
    assert variable.name == "a"
    assert variable.domain == {1, 2, 3}
    assert variable.value() == 1
    assert variable.is_assigned()
    variable.unassign()
    assert variable.value() is None
    assert not variable.is_assigned()


def test_revert():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))
    assert variable.name == "a"
    assert variable.value() is None
    assert variable.domain == {1, 2, 3}
    assert not variable.is_assigned()
    variable.assign(1)
    assert variable.value() == 1
    variable.unassign()
    assert variable.value() is None
    variable.revert()
    assert variable.value() == 1
    variable.revert()
    assert variable.value() is None


def test_invalid_delta_records():
    with pytest.raises(Variable.Error):
        Variable(DeltaRecord(), "a", Domain(DeltaRecord(), {1, 2, 3}))


def test_domain_values():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))
    assert variable.domain == {1, 2, 3}
    assert variable.domain_values() == {1, 2, 3}


def test_add_value_to_domain():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))
    assert variable.domain == {1, 2, 3}
    assert variable.domain_values() == {1, 2, 3}
    variable.add_value_to_domain(4)
    assert variable.domain == {1, 2, 3, 4}
    assert variable.domain_values() == {1, 2, 3, 4}
    variable.revert()
    assert variable.domain == {1, 2, 3}
    assert variable.domain_values() == {1, 2, 3}


def test_remove_value_from_domain():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))
    assert variable.domain == {1, 2, 3}
    assert variable.domain_values() == {1, 2, 3}
    variable.remove_value_from_domain(2)
    assert variable.domain == {1, 3}
    assert variable.domain_values() == {1, 3}
    variable.revert()
    assert variable.domain == {1, 2, 3}
    assert variable.domain_values() == {1, 2, 3}


def test_remove_invalid_value_from_domain():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1}))
    with pytest.raises(Variable.DomainError):
        variable.remove_value_from_domain(2)


def test_domain_size():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))
    assert variable.domain == {1, 2, 3}
    assert variable.domain_size() == 3


def test_add_duplicate_value_to_domain():
    delta_record = DeltaRecord()
    variable = Variable(delta_record, "a", Domain(delta_record, {1}))
    variable.add_value_to_domain(1)  # should be a no-op
    assert variable.domain == {1}
    variable.revert()
    assert variable.domain == {1}
