from .all_different_constraint import AllDifferentConstraint
from .csp import CSP


def test_constraints_for():
    c1 = AllDifferentConstraint(frozenset({"a", "b"}))
    c2 = AllDifferentConstraint(frozenset({"b", "c"}))
    csp = CSP.for_constraints(c1, c2)

    assert set(csp.constraints_for("a")) == {c1}
    assert set(csp.constraints_for("b")) == {c1, c2}
    assert set(csp.constraints_for("z")) == set()
