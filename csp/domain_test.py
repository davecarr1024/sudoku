from .domain import Domain


def test_len(subtests):
    for domain, expected in list[tuple[Domain[int], int]](
        [
            (
                Domain[int](),
                0,
            ),
            (
                Domain[int](frozenset({1, 2, 3})),
                3,
            ),
        ]
    ):
        with subtests.test(domain=domain, expected=expected):
            assert len(domain) == expected


def test_contains(subtests):
    for domain, value, expected in list[tuple[Domain[int], int, bool]](
        [
            (
                Domain[int](),
                1,
                False,
            ),
            (
                Domain[int](frozenset({1})),
                2,
                False,
            ),
            (
                Domain[int](frozenset({1})),
                1,
                True,
            ),
        ]
    ):
        with subtests.test(domain=domain, value=value, expected=expected):
            assert (value in domain) == expected


def test_and(subtests):
    for lhs, rhs, expected in list[tuple[Domain[int], Domain[int], Domain[int]]](
        [
            (
                Domain[int](),
                Domain[int](),
                Domain[int](),
            ),
            (
                Domain[int](frozenset({1, 2})),
                Domain[int](frozenset({2, 3})),
                Domain[int](frozenset({2})),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs & rhs == expected


def test_or(subtests):
    for lhs, rhs, expected in list[tuple[Domain[int], Domain[int], Domain[int]]](
        [
            (
                Domain[int](),
                Domain[int](),
                Domain[int](),
            ),
            (
                Domain[int](frozenset({1, 2})),
                Domain[int](frozenset({2, 3})),
                Domain[int](frozenset({1, 2, 3})),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs | rhs == expected


def test_sub(subtests):
    for lhs, rhs, expected in list[tuple[Domain[int], Domain[int], Domain[int]]](
        [
            (
                Domain[int](),
                Domain[int](),
                Domain[int](),
            ),
            (
                Domain[int](frozenset({1, 2})),
                Domain[int](frozenset({2, 3})),
                Domain[int](frozenset({1})),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs - rhs == expected


def test_with_value():
    assert Domain[int]().with_value(1) == Domain[int](frozenset({1}))


def test_without_value():
    assert Domain[int](frozenset({1})).without_value(1) == Domain[int]()
