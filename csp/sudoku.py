from dataclasses import dataclass, field, replace
from collections.abc import Mapping
from typing import Iterator, override, Self, Optional
import math
from .csp import CSP
from .state import State
from .search_strategy import SearchStrategy
from .solver_stats import SolverStats
from .all_different_constraint import AllDifferentConstraint
from .constraint import Constraint
from .variable import Variable


@dataclass(frozen=True)
class Sudoku(Mapping[tuple[int, int], int]):
    class Error(Exception): ...

    class KeyError(KeyError, Error): ...

    class ValueError(ValueError, Error): ...

    class SolveError(Error): ...

    size: int = 4
    clues: Mapping[tuple[int, int], int] = field(default_factory=dict)

    def _validate_key(self, key: tuple[int, int]) -> None:
        row, col = key
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            raise self.KeyError(f"Invalid key: {key}")

    @override
    def __getitem__(self, key: tuple[int, int]) -> int:
        self._validate_key(key)
        return self.clues.get(key, 0)

    @override
    def __iter__(self) -> Iterator[tuple[int, int]]:
        for row in range(self.size):
            for col in range(self.size):
                yield (row, col)

    @override
    def __len__(self) -> int:
        return self.size * self.size

    @override
    def __str__(self) -> str:
        lines = []
        for row in range(self.size):
            line = " ".join(str(self[row, col]) or "." for col in range(self.size))
            lines.append(line)
        return "\n".join(lines)

    def with_value(self, key: tuple[int, int], value: int) -> Self:
        self._validate_key(key)
        return replace(self, clues=self.clues | {key: value})

    @staticmethod
    def _key_to_var_name(key: tuple[int, int]) -> str:
        row, col = key
        return f'{chr(ord("A")+row)}{col+1}'

    @staticmethod
    def _var_name_to_key(var_name: str) -> tuple[int, int]:
        row = ord(var_name[0]) - ord("A")
        col = int(var_name[1]) - 1
        return (row, col)

    def make_csp(self) -> tuple[CSP[int], State[int]]:
        square_size = math.isqrt(self.size)
        if square_size * square_size != self.size:
            raise self.ValueError(f"Invalid size: {self.size}, must be a square")
        constraints = list[Constraint[int]]()
        for row in range(self.size):
            constraints.append(
                AllDifferentConstraint(
                    frozenset(
                        {self._key_to_var_name((row, col)) for col in range(self.size)}
                    )
                )
            )
        for col in range(self.size):
            constraints.append(
                AllDifferentConstraint(
                    frozenset(
                        {self._key_to_var_name((row, col)) for row in range(self.size)}
                    )
                )
            )
        for start_row in range(0, self.size, square_size):
            for start_col in range(0, self.size, square_size):
                constraints.append(
                    AllDifferentConstraint(
                        frozenset(
                            {
                                self._key_to_var_name((row, col))
                                for row in range(start_row, start_row + square_size)
                                for col in range(start_col, start_col + square_size)
                            }
                        )
                    )
                )
        csp = CSP(constraints)
        state = State()
        for row in range(self.size):
            for col in range(self.size):
                state = state.with_variable(
                    Variable.make(
                        self._key_to_var_name((row, col)),
                        *range(1, self.size + 1),
                        assigned=self[row, col] or None,
                    )
                )
        return csp, state

    def solve(self, strategy: SearchStrategy[int]) -> tuple[SolverStats, Self]:
        csp, state = self.make_csp()
        stats, result = strategy.solve(csp, state)

        if result is None:
            raise self.SolveError(f"No solution found for {self}")

        if not csp.is_satisfied(result):
            raise self.SolveError(f"Returned solution {result} violates constraints")

        # Reconstruct solved Sudoku
        solved = self
        for variable in result.values():
            if not variable.is_assigned():
                raise self.SolveError(f"Unassigned variable in solution: {variable}")

            row, col = self._var_name_to_key(variable.name)
            solved = solved.with_value((row, col), variable.value)

        return stats, solved

    @classmethod
    def from_grid(cls, size: int, grid: list[list[Optional[int]]]) -> Self:
        clues = dict[tuple[int, int], int]()
        for row, cols in enumerate(grid):
            for col, value in enumerate(cols):
                if row >= size or col >= size:
                    raise cls.ValueError(f"Invalid grid entry: {row},{col} = {value}")
                if value is not None:
                    clues[(row, col)] = value
        return cls(size, clues)

    @classmethod
    def from_str(cls, size: int, sudoku_str: str) -> Self:
        grid = list[list[int]]()
        for row, line in enumerate(sudoku_str.strip().splitlines()):
            cols = list[int]()
            for col, value in enumerate(line.split()):
                if value == ".":
                    cols.append(None)
                else:
                    cols.append(int(value))
            grid.append(cols)
        return cls.from_grid(size, grid)
