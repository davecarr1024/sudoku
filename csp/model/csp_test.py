from csp.model import CSP
from csp.model.constraints import AllDifferent
from csp.delta import DeltaRecord
from csp.state import State, Variable, Domain


def test_collection():
    c1 = AllDifferent[int]({"a", "b"})
    c2 = AllDifferent[int]({"b", "c"})
    csp = CSP[int]([c1, c2])
    assert csp == {c1, c2}
    assert len(csp) == 2
    assert csp.constraints() == {c1, c2}


def test_constraints_for():
    c1 = AllDifferent[int]({"a", "b"})
    c2 = AllDifferent[int]({"b", "c"})
    csp = CSP[int]([c1, c2])
    assert csp.constraints_for("a") == {c1}
    assert csp.constraints_for("b") == {c1, c2}
    assert csp.constraints_for("c") == {c2}


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
    assert csp.constraints_for("d") == set()


def test_constraints_between():
    c1 = AllDifferent[int]({"a", "b"})
    c2 = AllDifferent[int]({"b", "c"})
    csp = CSP[int]([c1, c2])
    assert csp.constraints_between("a", "b") == {c1}
    assert csp.constraints_between("b", "c") == {c2}
    assert csp.constraints_between("a", "c") == set()


def test_neighbors():
    c1 = AllDifferent[int]({"a", "b"})
    c2 = AllDifferent[int]({"b", "c"})
    csp = CSP[int]([c1, c2])
    assert csp.neighbors("a") == {"b"}
    assert csp.neighbors("b") == {"a", "c"}
    assert csp.neighbors("c") == {"b"}
