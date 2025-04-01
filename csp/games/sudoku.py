from csp.games.game import Game
from csp.model import CSP, Constraint
from csp.model.constraints import AllDifferent
from csp.state import State, Variable, Domain
from csp.delta import DeltaRecord
from typing import override, Iterable, Iterator
import math
from collections.abc import MutableMapping, Mapping


class Sudoku(Game[int], MutableMapping[tuple[int, int], int]):
    class Error(Game[int].Error): ...

    @staticmethod
    def _key_to_var(key: tuple[int, int]) -> str:
        return f'{chr(ord("A")+key[0])}{key[1]+1}'

    @staticmethod
    def _var_to_key(var: str) -> tuple[int, int]:
        return (ord(var[0]) - ord("A"), int(var[1]) - 1)

    @classmethod
    def _make_csp(cls, size: int) -> CSP[int]:
        cls._validate_size(size)
        square_size = math.isqrt(size)

        def _constraints_for_squares() -> Iterable[Constraint[int]]:
            for start_row in range(0, size, square_size):
                for start_col in range(0, size, square_size):
                    yield AllDifferent[int](
                        {
                            cls._key_to_var((row, col))
                            for row in range(start_row, start_row + square_size)
                            for col in range(start_col, start_col + square_size)
                        }
                    )

        def _constraints_for_rows() -> Iterable[Constraint[int]]:
            for row in range(size):
                yield AllDifferent[int](
                    {cls._key_to_var((row, col)) for col in range(size)}
                )

        def _constraints_for_cols() -> Iterable[Constraint[int]]:
            for col in range(size):
                yield AllDifferent[int](
                    {cls._key_to_var((row, col)) for row in range(size)}
                )

        return CSP[int](
            list(_constraints_for_squares())
            + list(_constraints_for_rows())
            + list(_constraints_for_cols())
        )

    @staticmethod
    def _validate_size(size: int) -> None:
        square_size = math.isqrt(size)
        if square_size * square_size != size:
            raise Sudoku.Error(f"size {size} must be a square")

    def _validate_key(self, key: tuple[int, int]) -> None:
        row, col = key
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            raise self.Error(f"key {key} is out of bounds {self.size}x{self.size}")

    def _validate_value(self, value: int) -> None:
        if value < 0 or value > self.size:
            raise self.Error(f"value {value} is out of bounds {self.size}")

    def __init__(self, size: int, values: Mapping[tuple[int, int], int]) -> None:
        Sudoku._validate_size(size)
        self.size = size
        for key, value in values.items():
            self._validate_key(key)
            self._validate_value(value)
        self._values = dict(values)

    @override
    def __iter__(self) -> Iterator[tuple[int, int]]:
        for row in range(self.size):
            for col in range(self.size):
                yield (row, col)

    @override
    def __getitem__(self, key: tuple[int, int]) -> int:
        self._validate_key(key)
        return self._values.get(key, 0)

    @override
    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self._validate_key(key)
        self._validate_value(value)
        self._values[key] = value

    @override
    def __delitem__(self, key: tuple[int, int]) -> None:
        self._validate_key(key)
        if key in self._values:
            del self._values[key]

    @override
    def __len__(self) -> int:
        return self.size**2

    @override
    def to_state(self) -> tuple[CSP[int], State[int]]:
        delta_record = DeltaRecord()
        return (
            self._make_csp(self.size),
            State[int](
                delta_record,
                [
                    Variable[int](
                        delta_record,
                        self._key_to_var((row, col)),
                        Domain[int](delta_record, set(range(1, self.size + 1))),
                        value if value != 0 else None,
                    )
                    for (row, col), value in self.items()
                ],
            ),
        )

    @override
    @classmethod
    def from_state(cls, csp: CSP[int], state: State[int]) -> "Sudoku":
        def _vals() -> Iterable[tuple[tuple[int, int], int]]:
            for key, var in state.items():
                val = var.value()
                if val is None:
                    continue
                yield (cls._var_to_key(var.name), val)

        size = max(
            max(row + 1, col + 1)
            for row, col in [cls._var_to_key(var) for var in state]
        )

        return Sudoku(
            size,
            dict(_vals()),
        )

    @override
    def __str__(self) -> str:
        def _val_str(row, col) -> str:
            val = self[row, col]
            if val == 0:
                return "."
            else:
                return str(val)

        result = ""
        for row in range(self.size):
            result += " ".join(_val_str(row, col) for col in range(self.size))
            result += "\n"
        return result

    @classmethod
    def from_str(cls, sudoku_string: str) -> "Sudoku":
        def _val(val: str) -> int:
            if val == ".":
                return 0
            else:
                return int(val)

        vals: list[list[int]] = [
            [_val(val) for val in line.split()]
            for line in sudoku_string.strip().splitlines()
        ]
        size = len(vals)
        cls._validate_size(size)
        for i, line in enumerate(vals):
            if len(line) != size:
                raise cls.Error(
                    f"invalid sudoku string: line {i} has wrong length: should be {size}"
                )
        return Sudoku(
            size,
            {
                (row, col): value
                for row, row_vals in enumerate(vals)
                for col, value in enumerate(row_vals)
            },
        )
