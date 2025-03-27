import pytest
from typing import Optional
from .sudoku import Sudoku
from .variable import Variable
from .search_strategy import SearchStrategy
from .depth_first_search import DepthFirstSearch
from .ac3_propagator import AC3Propagator


def test_getitem(subtests):
    for sudoku, key, expected in list[
        tuple[
            Sudoku,
            tuple[int, int],
            Optional[int],
        ]
    ](
        [
            (
                Sudoku(),
                (0, 0),
                0,
            ),
            (
                Sudoku(),
                (-1, -1),
                None,
            ),
            (
                Sudoku(clues={(0, 0): 1}),
                (0, 0),
                1,
            ),
        ]
    ):
        with subtests.test(sudoku=sudoku, expected=expected):
            if expected is None:
                with pytest.raises(Sudoku.KeyError):
                    _ = sudoku[key]
            else:
                assert sudoku[key] == expected


def test_with_value(subtests):
    for sudoku, key, value, expected in list[
        tuple[
            Sudoku,
            tuple[int, int],
            int,
            Optional[Sudoku],
        ]
    ](
        [
            (
                Sudoku(),
                (0, 0),
                1,
                Sudoku(clues={(0, 0): 1}),
            ),
            (
                Sudoku(),
                (-1, 0),
                1,
                None,
            ),
        ]
    ):
        with subtests.test(sudoku=sudoku, key=key, value=value, expected=expected):
            if expected is None:
                with pytest.raises(Sudoku.KeyError):
                    _ = sudoku.with_value(key, value)
            else:
                assert sudoku.with_value(key, value) == expected


def test_empty():
    assert list(Sudoku().values()) == [0] * 16


def test_make_csp():
    sudoku = Sudoku().with_value((0, 0), 1).with_value((0, 1), 2)
    csp, state = sudoku.make_csp()
    constraint_sets = [c.variables for c in csp.constraints]

    # Assert correct number of constraints: 4 rows + 4 cols + 4 boxes = 12
    assert len(constraint_sets) == 12

    # Assert rows are present
    assert frozenset({"A1", "A2", "A3", "A4"}) in constraint_sets
    assert frozenset({"D1", "D2", "D3", "D4"}) in constraint_sets

    # Assert columns are present
    assert frozenset({"A1", "B1", "C1", "D1"}) in constraint_sets
    assert frozenset({"A4", "B4", "C4", "D4"}) in constraint_sets

    # Assert boxes are present
    assert frozenset({"A1", "A2", "B1", "B2"}) in constraint_sets
    assert frozenset({"C3", "C4", "D3", "D4"}) in constraint_sets

    # Assert clue variables are assigned in state
    assert Variable.make("A1", 1, 2, 3, 4, assigned=1) in state.values()
    assert Variable.make("A2", 1, 2, 3, 4, assigned=2) in state.values()


def test_make_csp_not_square():
    with pytest.raises(Sudoku.ValueError):
        Sudoku(size=5).make_csp()


def test_from_grid(subtests):
    for size, grid, expected in list[
        int,
        tuple[
            list[list[int]],
            Optional[Sudoku],
        ],
    ](
        [
            (
                4,
                [
                    [1, 2, 3, 4],
                    [5, 6, 7],
                    [None, 8, 9],
                ],
                Sudoku(
                    size=4,
                    clues={
                        (0, 0): 1,
                        (0, 1): 2,
                        (0, 2): 3,
                        (0, 3): 4,
                        (1, 0): 5,
                        (1, 1): 6,
                        (1, 2): 7,
                        (2, 1): 8,
                        (2, 2): 9,
                    },
                ),
            ),
            (
                4,
                [
                    [1, 2, 3, 4, 5],
                ],
                None,
            ),
            (
                4,
                [
                    [],
                    [],
                    [],
                    [],
                    [1],
                ],
                None,
            ),
        ]
    ):
        with subtests.test(grid=grid, expected=expected):
            if expected is None:
                with pytest.raises(Sudoku.ValueError):
                    Sudoku.from_grid(size, grid)
            else:
                assert Sudoku.from_grid(size, grid) == expected


def test_from_str(subtests):
    for size, sudoku_str, expected in list[
        tuple[
            int,
            str,
            Optional[Sudoku],
        ]
    ](
        [
            (
                4,
                """
                1 2 3 4
                5 6 7 .
                . 8 9
                """,
                Sudoku(
                    size=4,
                    clues={
                        (0, 0): 1,
                        (0, 1): 2,
                        (0, 2): 3,
                        (0, 3): 4,
                        (1, 0): 5,
                        (1, 1): 6,
                        (1, 2): 7,
                        (2, 1): 8,
                        (2, 2): 9,
                    },
                ),
            ),
            (
                4,
                "1 2 3 4 5",
                None,
            ),
            (
                4,
                """
                .
                .
                .
                .
                1
                """,
                None,
            ),
        ]
    ):
        with subtests.test(sudoku_str=sudoku_str, expected=expected):
            if expected is None:
                with pytest.raises(Sudoku.ValueError):
                    Sudoku.from_str(size, sudoku_str)
            else:
                assert Sudoku.from_str(size, sudoku_str) == expected


def test_solve(subtests):
    for strategy in list[SearchStrategy[int]](
        [
            DepthFirstSearch(AC3Propagator()),
        ]
    ):
        for name, sudoku, expected_cells in list[
            tuple[
                str,
                Sudoku,
                Optional[dict[tuple[int, int], int]],
            ]
        ](
            [
                (
                    "4x4 invalid duplicate in row",
                    Sudoku(size=4).with_value((0, 0), 1).with_value((0, 1), 1),
                    None,
                ),
                (
                    "4x4 invalid duplicate in box",
                    Sudoku(size=4)
                    .with_value((0, 0), 2)
                    .with_value((1, 1), 2),  # both in top-left box
                    None,
                ),
                (
                    "box deduction",
                    Sudoku(size=4)
                    .with_value((0, 0), 1)
                    .with_value((0, 1), 2)
                    .with_value((1, 0), 3),
                    {(1, 1): 4},
                ),
                (
                    "row deduction",
                    Sudoku(size=4)
                    .with_value((2, 0), 1)
                    .with_value((2, 1), 2)
                    .with_value((2, 2), 3),
                    {(2, 3): 4},
                ),
                (
                    "column deduction",
                    Sudoku(size=4)
                    .with_value((0, 2), 4)
                    .with_value((1, 2), 3)
                    .with_value((2, 2), 2),
                    {(3, 2): 1},
                ),
                # (
                #     "9x9 easy puzzle",
                #     Sudoku.from_str(
                #         9,
                #         """
                #         5 3 . . 7 . . . .
                #         6 . . 1 9 5 . . .
                #         . 9 8 . . . . 6 .
                #         8 . . . 6 . . . 3
                #         4 . . 8 . 3 . . 1
                #         7 . . . 2 . . . 6
                #         . 6 . . . . 2 8 .
                #         . . . 4 1 9 . . 5
                #         . . . . 8 . . 7 9
                #         """,
                #     ),
                #     {
                #         (0, 0): 5,
                #         (0, 1): 3,
                #         (1, 3): 1,
                #         (8, 8): 9,
                #         # You can add more assertions if you want to be more rigorous
                #     },
                # ),
            ]
        ):
            with subtests.test(
                name=name,
                expected_cells=expected_cells,
                sudoku=sudoku,
                strategy=strategy,
            ):
                if expected_cells is None:
                    try:
                        stats, solution = sudoku.solve(strategy)
                        assert False, f"unexpectedly solved {name}: {stats} {solution}"
                    except Sudoku.SolveError:
                        pass
                else:
                    stats, solution = sudoku.solve(strategy)
                    for key, value in expected_cells.items():
                        assert solution[key] == value
                    print(f"{name}: {stats}")
