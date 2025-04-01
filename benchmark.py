from csp.games import Sudoku
from csp.processing import SearchStrategy
from csp.processing.strategies import DepthFirstSearch
from csp.processing.propagators import NullPropagator, SimplePropagator, AC3

# === Define Benchmark Puzzles ===
puzzles = [
    (
        "4x4-already-solved",
        Sudoku.from_str(
            """
            1 2 3 4
            3 4 1 2
            4 1 2 3
            2 3 4 1
            """
        ),
    ),
    (
        "4x4-almost-solved",
        Sudoku.from_str(
            """
            1 2 3 .
            3 4 1 2
            4 1 2 3
            2 3 4 1
            """
        ),
    ),
    (
        "4x4-empty",
        Sudoku.from_str(
            """
            . . . .
            . . . .
            . . . .
            . . . .
            """
        ),
    ),
    (
        "4x4-simple",
        Sudoku.from_str(
            """
            . 2 . 4
            . . . .
            . . . .
            1 . 3 .
            """
        ),
    ),
    (
        "9x9-easy",
        Sudoku.from_str(
            """
            1 2 . . . . . . .
            . . . . . . . . .
            . . . . . . . . .
            . . . . . . . . .
            . . . . . . . . .
            . . . . . . . . .
            . . . . . . . . .
            . . . . . . . . .
            . . . . . . . . 3
            """
        ),
    ),
]

# === Define Search Strategies ===
strategies: list[tuple[str, SearchStrategy[int]]] = [
    (
        "DFS + NullPropagator",
        DepthFirstSearch(
            NullPropagator(),
        ),
    ),
    (
        "DFS + SimplePropagator",
        DepthFirstSearch(
            SimplePropagator(),
        ),
    ),
(
    "DFS + AC3",
    DepthFirstSearch(
        AC3(),
    ),
),
]


# === Run Benchmark ===
def run_benchmark():
    for strategy_name, strategy in strategies:
        print(f"\n=== Strategy: {strategy_name} ===")
        total_stats = SearchStrategy.Stats()

        for puzzle_name, puzzle in puzzles:
            print(f"\n--- Puzzle: {puzzle_name} ---")
            try:
                result, stats = puzzle.solve(strategy)
                print(puzzle)
                print(result)
                print(stats)
                total_stats += stats
            except Sudoku.Error as e:
                print(f"Failed to solve '{puzzle_name}': {e}")

        print(f"\n>>> TOTAL for strategy '{strategy_name}':\n{total_stats}")


if __name__ == "__main__":
    run_benchmark()
