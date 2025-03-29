from .csp import CSP
from .all_different import AllDifferent
from .delta_record import DeltaRecord
from .state import State
from .variable import Variable
from .domain import Domain


def test_collection():
    c1 = AllDifferent[int]({"a", "b"})
    c2 = AllDifferent[int]({"b", "c"})
    csp = CSP[int]([c1, c2])
    assert set(csp) == {c1, c2}
    assert len(csp) == 2
    assert set(csp.constraints()) == {c1, c2}


def test_constraints_for():
    c1 = AllDifferent[int]({"a", "b"})
    c2 = AllDifferent[int]({"b", "c"})
    csp = CSP[int]([c1, c2])
    assert set(csp.constraints_for("a")) == {c1}
    assert set(csp.constraints_for("b")) == {c1, c2}
    assert set(csp.constraints_for("c")) == {c2}


def test_is_satisfied():
    delta_record = DeltaRecord()
    c1 = AllDifferent[int]({"a", "b"})
    c2 = AllDifferent[int]({"b", "c"})
    csp = CSP[int]([c1, c2])
    assert csp.is_satisfied(
        State(
            delta_record,
            [
                Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}), 1),
                Variable(delta_record, "b", Domain(delta_record, {1, 2, 3}), 2),
                Variable(delta_record, "c", Domain(delta_record, {1, 2, 3}), 3),
            ],
        )
    )
    assert not csp.is_satisfied(
        State(
            delta_record,
            [
                Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}), 1),
                Variable(delta_record, "b", Domain(delta_record, {1, 2, 3}), 2),
                Variable(delta_record, "c", Domain(delta_record, {1, 2, 3}), 2),
            ],
        )
    )


def test_constraints_for_unknown_var():
    csp = CSP[int]([AllDifferent({"a", "b"})])
    assert csp.constraints_for("d") == []
