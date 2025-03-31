from csp.state.domain import Domain
from csp.delta import DeltaRecord
import pytest


def test_add_value():
    domain = Domain(DeltaRecord(), set())
    domain.add_value(1)
    assert set(domain) == {1}
    domain.revert()
    assert set(domain) == set()


def test_add_value_in_context():
    delta_record = DeltaRecord()
    domain = Domain(delta_record, set())
    with delta_record.maintain_state():
        domain.add_value(1)
        assert set(domain) == {1}
    assert set(domain) == set()


def test_multiple_values():
    delta_record = DeltaRecord()
    domain = Domain(delta_record, set())
    with delta_record.maintain_state():
        domain.add_value(1)
        domain.add_value(2)
        assert set(domain) == {1, 2}
    assert set(domain) == set()


def test_partial_revert():
    delta_record = DeltaRecord()
    domain = Domain(delta_record, set())
    domain.add_value(1)
    assert set(domain) == {1}
    with delta_record.maintain_state():
        domain.add_value(2)
        domain.remove_value(1)
        assert set(domain) == {2}
    assert set(domain) == {1}


def test_remove_value():
    domain = Domain(DeltaRecord(), {1})
    domain.remove_value(1)
    assert set(domain) == set()
    domain.revert()
    assert set(domain) == {1}


def test_double_remove():
    domain = Domain(DeltaRecord(), {1})
    domain.remove_value(1)
    with pytest.raises(Domain.Error):
        domain.remove_value(1)


def test_double_add():
    domain = Domain(DeltaRecord(), set())
    domain.add_value(1)
    assert set(domain) == {1}
    domain.add_value(1)
    assert set(domain) == {1}
    domain.revert()
    assert set(domain) == {1}
    domain.revert()
    assert set(domain) == set()


def test_delta_underflow():
    domain = Domain(DeltaRecord(), set())
    with pytest.raises(DeltaRecord.Error):
        domain.revert()
