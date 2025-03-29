#!/home/runner/workspace/.pythonlibs/bin/python3.13

from csp.sudoku import Sudoku
from csp.depth_first_search import DepthFirstSearch
from csp.ac3_propagator import AC3Propagator
from csp.search_strategy import SearchStrategy
from csp.solver_stats import SolverStats

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
    # (
    #     "9x9 AI Escargot (very hard)",
    #     Sudoku.from_str(
    #         9,
    #         """
    #     1 . . . . 7 . 9 .
    #     . 3 . . 2 . . . 8
    #     . . 9 6 . . 5 . .
    #     . . 5 3 . . 9 . .
    #     . 1 . . 8 . . . 2
    #     6 . . . . 4 . . .
    #     3 . . . . . . 1 .
    #     . 4 . . . . . . 7
    #     . . 7 . . . 3 . .
    #     """,
    #     ),
    # ),
]


strategies: list[SearchStrategy[int]] = [
    # DepthFirstSearch(
    #     AC3Propagator(),
    #     minimum_remaining_values=False,
    #     least_constraining_values=False,
    # ),
    # DepthFirstSearch(
    #     AC3Propagator(),
    #     minimum_remaining_values=False,
    #     least_constraining_values=True,
    # ),
    # DepthFirstSearch(
    #     AC3Propagator(),
    #     minimum_remaining_values=True,
    #     least_constraining_values=False,
    # ),
    DepthFirstSearch(
        AC3Propagator(),
        minimum_remaining_values=True,
        least_constraining_values=True,
    ),
]


def run_benchmarks():
    for strategy in strategies:
        print(f"\n== Strategy: {strategy} ==")
        strategy_stats = SolverStats()
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
                strategy_stats = strategy_stats.merge(stats)
                strategy_stats.elapsed_time += stats.elapsed_time
            except Sudoku.SolveError as e:
                print(f"  Failed to solve: {e}\n")
        print(f"{strategy} total stats: {strategy_stats}")


if __name__ == "__main__":
    run_benchmarks()
