from csp.sudoku import Sudoku
from csp.depth_first_search import DepthFirstSearch
from csp.ac3_propagator import AC3Propagator
from csp.search_strategy import SearchStrategy


benchmark_cases: list[tuple[str, Sudoku]] = [
    (
        "9x9 easy puzzle",
        Sudoku.from_str(
            9,
            """
            5 3 . . 7 . . . .
            6 . . 1 9 5 . . .
            . 9 8 . . . . 6 .
            8 . . . 6 . . . 3
            4 . . 8 . 3 . . 1
            7 . . . 2 . . . 6
            . 6 . . . . 2 8 .
            . . . 4 1 9 . . 5
            . . . . 8 . . 7 9
            """,
        ),
    ),
    # Add more cases as needed
]


strategies: list[SearchStrategy[int]] = [
    DepthFirstSearch(
        AC3Propagator(),
        use_minimum_remaining_values=False,
    ),
    DepthFirstSearch(
        AC3Propagator(),
        use_minimum_remaining_values=True,
    ),
]


def run_benchmarks():
    for strategy in strategies:
        print(f"\n== Strategy: {strategy} ==")
        for name, sudoku in benchmark_cases:
            print(f"Puzzle: {name}")
            try:
                stats, solution = sudoku.solve(strategy)
                print(f"  Elapsed Time: {stats.elapsed_time:.4f} seconds")
                print(f"  Assignments: {stats.assignments}")
                print(f"  State Visits: {stats.state_visits}")
                print(f"  Propagations: {stats.propagations}")
                print(f"  Max Depth: {stats.max_depth}")
                print()
            except Sudoku.SolveError as e:
                print(f"  Failed to solve: {e}\n")


if __name__ == "__main__":
    run_benchmarks()
