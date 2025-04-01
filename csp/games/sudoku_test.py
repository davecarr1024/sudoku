from csp.games import Sudoku
from csp.state import State, Variable, Domain
from csp.delta import DeltaRecord
from csp.model import CSP
from csp.processing import SearchStrategy
from csp.processing.strategies import DepthFirstSearch
from csp.processing.propagators import NullPropagator, SimplePropagator, AC3
import pytest
from collections.abc import Mapping
from typing import Optional


def test_create_empty():
    assert Sudoku(4, {}) == {(row, col): 0 for row in range(4) for col in range(4)}


def test_create():
    assert Sudoku(4, {(1, 2): 3}) == {
        (row, col): 0 for row in range(4) for col in range(4)
    } | {(1, 2): 3}


def test_create_invalid_size():
    with pytest.raises(Sudoku.Error):
        Sudoku(5, {})


def test_create_invalid_key():
    with pytest.raises(Sudoku.Error):
        Sudoku(4, {(-1, 2): 3})


def test_create_invalid_value():
    with pytest.raises(Sudoku.Error):
        Sudoku(4, {(1, 2): 5})


def test_set():
    sudoku = Sudoku(4, {(1, 2): 3})
    assert sudoku[(1, 2)] == 3
    sudoku[(1, 2)] = 1
    assert sudoku[(1, 2)] == 1


def test_set_invalid_key():
    with pytest.raises(Sudoku.Error):
        Sudoku(4, {})[-1, 2] = 3


def test_set_invalid_value():
    with pytest.raises(Sudoku.Error):
        Sudoku(4, {})[(1, 2)] = 5


def test_del():
    sudoku = Sudoku(4, {(1, 2): 3})
    del sudoku[(1, 2)]
    assert sudoku[(1, 2)] == 0


def test_del_invalid_key():
    with pytest.raises(Sudoku.Error):
        del Sudoku(4, {})[-1, 2]


def test_del_redundant():
    sudoku = Sudoku(4, {})
    del sudoku[(1, 2)]
    assert sudoku[(1, 2)] == 0


def test_len():
    assert len(Sudoku(4, {})) == 16


def test_str():
    assert " 3 " in str(Sudoku(4, {(1, 2): 3}))


def test_from_str():
    assert (
        Sudoku.from_str(
            """
        1 . . .
        . 2 . .
        . . 3 .
        . . . 4
        """
        )
        == Sudoku(4, {(0, 0): 1, (1, 1): 2, (2, 2): 3, (3, 3): 4})
    )


def test_from_str_invalid_size():
    with pytest.raises(Sudoku.Error):
        Sudoku.from_str("1 2 3 4")


def test_from_str_mismatched_size():
    with pytest.raises(Sudoku.Error):
        Sudoku.from_str("1 2 3 4\n5\n6\n7\n")


def test_to_state_and_back():
    sudoku = Sudoku(4, {(0, 0): 1, (1, 1): 2, (2, 2): 3, (3, 3): 4})
    csp, state = sudoku.to_state()
    restored = sudoku.from_state(csp, state)

    assert restored == sudoku


def test_to_state_correct_variables():
    sudoku = Sudoku(4, {(0, 0): 1, (1, 1): 2})
    csp, state = sudoku.to_state()
    assert state["A1"].value() == 1
    assert state["B2"].value() == 2


def test_make_csp():
    csp, state = Sudoku(4, {}).to_state()
    assert {
        var for constraint in csp.constraints() for var in constraint.variables()
    } == {f"{row}{col}" for row in "ABCD" for col in "1234"}


def test_from_state_only_filled_values():
    delta_record = DeltaRecord()
    state = State(
        delta_record,
        [
            Variable(
                delta_record,
                "A1",
                Domain(delta_record, set(range(1, 5))),
                1,
            ),
            Variable(
                delta_record,
                "B2",
                Domain(delta_record, set(range(1, 5))),
                2,
            ),
            Variable(
                delta_record,
                "D4",
                Domain(delta_record, set(range(1, 5))),
            ),  # unassigned
        ],
    )

    restored = Sudoku.from_state(CSP[int]([]), state)

    assert restored[(0, 0)] == 1
    assert restored[(1, 1)] == 2
    assert restored[(3, 3)] == 0  # unassigned -> 0


def test_to_state_var_names():
    csp, state = Sudoku(4, {}).to_state()
    vars = state.keys()
    assert len(vars) == 16
    assert set(vars) == {f"{row}{col}" for row in "ABCD" for col in "1234"}


def test_solve(subtests):
    for strategy in list[SearchStrategy[int]](
        [
            DepthFirstSearch(NullPropagator()),
            DepthFirstSearch(SimplePropagator()),
            DepthFirstSearch(AC3()),
        ]
    ):
        for name, game, expected in list[
            tuple[
                str,
                Sudoku,
                Optional[Mapping[tuple[int, int], int]],
            ]
        ](
            [
                (
                    "already-solved",
                    Sudoku.from_str(
                        """
                    1 2 3 4
                    3 4 1 2
                    4 1 2 3
                    2 3 4 1
                    """
                    ),
                    {},
                ),
                (
                    "almost-solved",
                    Sudoku.from_str(
                        """
                    1 2 3 .
                    3 4 1 2
                    4 1 2 3
                    2 3 4 1
                    """
                    ),
                    {},
                ),
                (
                    "empty",
                    Sudoku.from_str(
                        """
                    . . . .
                    . . . .
                    . . . .
                    . . . .
                    """
                    ),
                    {},
                ),
                (
                    "simple-4x4-solvable-a",
                    Sudoku.from_str(
                        """
                    . 2 . 4
                    . . . .
                    . . . .
                    1 . 3 .
                """
                    ),
                    {(0, 0): 3, (3, 3): 2},
                ),
                (
                    "4x4-contradiction-row-duplicate",
                    Sudoku.from_str(
                        """
                    2 2 . .
                    . . . .
                    . . . .
                    . . . .
                """
                    ),
                    None,
                ),
                (
                    "4x4-solvable-b",
                    Sudoku.from_str(
                        """
                    . . 1 .
                    . . . .
                    . 3 . .
                    4 . . .
                """
                    ),
                    {},
                ),
                (
                    "4x4-contradiction-square-duplicate",
                    Sudoku.from_str(
                        """
                    1 . . .
                    . 1 . .
                    . . . .
                    . . . .
                """
                    ),
                    None,
                ),
                (
                    "minimal-valid-4x4",
                    Sudoku.from_str(
                        """
                    . . . .
                    . . . .
                    . . . .
                    . 1 . .
                """
                    ),
                    {(3, 1): 1},  # Confirm that clue is preserved in result
                ),
                # (
                #     "9x9-easy",
                #     Sudoku.from_str(
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
                #         """
                #     ),
                #     {(0, 2): 4, (8, 0): 3},
                # ),
            ]
        ):
            with subtests.test(
                strategy=strategy,
                name=name,
                game=game,
                expected=expected,
            ):
                if expected is None:
                    with pytest.raises(Sudoku.Error):
                        game.solve(strategy)
                else:
                    result, _ = game.solve(strategy)
                    for key, val in expected.items():
                        assert result[key] == val, str(result)
                    assert result.satisfies_puzzle(game)
