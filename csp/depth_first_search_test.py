from .variable import Variable
from .state import State
from .all_different_constraint import AllDifferentConstraint
from .csp import CSP
from .ac3_propagator import AC3Propagator
from .depth_first_search import DepthFirstSearch


def test_dfs_solves_all_different():
    # Create variables A, B, C with domain {1, 2, 3}
    state = (
        State()
        .with_variable(Variable.make("A", 1, 2, 3))
        .with_variable(Variable.make("B", 1, 2, 3))
        .with_variable(Variable.make("C", 1, 2, 3))
    )

    # Constraint: all three must have different values
    csp = CSP.for_constraints(AllDifferentConstraint.for_vars("A", "B", "C"))

    # Solve
    propagator = AC3Propagator()
    dfs = DepthFirstSearch(propagator)
    stats, solution = dfs.solve(csp, state)

    # Validate solution
    assert solution is not None
    values = {v.name: v.value for v in solution.values()}
    assert sorted(values.keys()) == ["A", "B", "C"]
    assert all(value is not None for value in values.values())
    assert sorted(value for value in values.values() if value is not None) == [1, 2, 3]
    assert stats.max_depth == 3
    assert stats.assignments < 6
