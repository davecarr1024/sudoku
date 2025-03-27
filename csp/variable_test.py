from .variable import Variable
from .domain import Domain
import pytest
from typing import Optional


def test_is_assigned(subtests):
    for variable, expected in list[tuple[Variable, bool]](
        [
            (Variable("x", Domain.for_values(1, 2, 3)), False),
            (Variable("x", Domain.for_values(1, 2, 3), 1), True),
        ]
    ):
        with subtests.test(variable=variable, expected=expected):
            assert variable.is_assigned() == expected


def test_assign(subtests):
    for variable, value, expected in list[tuple[Variable, int, Optional[Variable]]](
        [
            (
                Variable("a", Domain.for_values(1, 2, 3)),
                4,
                None,
            ),
            (
                Variable("a", Domain.for_values(1, 2, 3)),
                1,
                Variable("a", Domain(frozenset({1})), 1),
            ),
        ]
    ):
        with subtests.test(variable=variable, value=value, expected=expected):
            if expected is None:
                with pytest.raises(Variable.ValueError):
                    variable.assign(value)
            else:
                assert variable.assign(value) == expected


def test_with_domain(subtests):
    for variable, domain, expected in list[tuple[Variable, Domain, Optional[Variable]]](
        [
            (
                Variable("a", Domain.for_values(1, 2, 3)),
                Domain.for_values(4, 5, 6),
                Variable("a", Domain.for_values(4, 5, 6)),
            ),
            (
                Variable("a", Domain.for_values(1, 2, 3), 1),
                Domain.for_values(4, 5, 6),
                None,
            ),
        ]
    ):
        with subtests.test(variable=variable, domain=domain, expected=expected):
            if expected is None:
                with pytest.raises(Variable.ValueError):
                    variable.with_domain(domain)
            else:
                assert variable.with_domain(domain) == expected


def test_make(subtests):
    for name, values, assigned, expected in list[
        tuple[
            str,
            list[int],
            Optional[int],
            Optional[Variable],
        ],
    ](
        [
            (
                "a",
                [1, 2, 3],
                4,
                None,
            ),
            (
                "a",
                [1, 2, 3],
                None,
                Variable("a", Domain.for_values(1, 2, 3)),
            ),
            (
                "a",
                [1, 2, 3],
                1,
                Variable("a", Domain.for_values(1, 2, 3), 1),
            ),
        ]
    ):
        with subtests.test(
            name=name,
            values=values,
            assigned=assigned,
            expected=expected,
        ):
            if expected is None:
                with pytest.raises(Variable.ValueError):
                    Variable.make(name, *values, assigned=assigned)
            else:
                assert Variable.make(name, *values, assigned=assigned)
