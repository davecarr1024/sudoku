from dataclasses import dataclass, field
from typing import Iterator, Iterable, override
from collections.abc import Mapping
from functools import cache
from .variable import Variable


@dataclass(frozen=True)
class State[T](Mapping[str, Variable[T]]):
    variables: frozenset[Variable[T]] = field(default_factory=frozenset)
    _cached_hash: int = field(
        init=False,
        repr=False,
        compare=False,
        hash=False,
    )
    _variable_cache: Mapping[str, Variable[T]] = field(
        init=False,
        repr=False,
        compare=False,
        hash=False,
    )

    @staticmethod
    @cache
    def _for_variables(variables: frozenset[Variable[T]]) -> "State[T]":
        return State[T](variables)

    @staticmethod
    def for_variables(*variables: Variable[T]) -> "State[T]":
        return State[T]._for_variables(frozenset(variables))

    def __post_init__(self) -> None:
        object.__setattr__(self, "_cached_hash", hash(self.values))
        object.__setattr__(self, "_variable_cache", {v.name: v for v in self.variables})

    @override
    def __hash__(self) -> int:
        return self._cached_hash

    @override
    def __len__(self) -> int:
        return len(self._variable_cache)

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._variable_cache)

    @override
    def __getitem__(self, key: str) -> Variable[T]:
        return self._variable_cache[key]

    def _with_variables(self, variables: frozenset[Variable[T]]) -> "State[T]":
        return State[T]._for_variables(variables)

    def with_variable(self, variable: Variable[T]) -> "State[T]":
        updated = dict(self._variable_cache)
        updated[variable.name] = variable
        return self._with_variables(frozenset(updated.values()))

    def is_valid(self) -> bool:
        return all(var.is_valid() for var in self.variables)

    def unassigned_variables(self) -> Iterable[Variable[T]]:
        return (v for v in self.variables if not v.is_assigned())

    def assign(self, variable_name: str, value: T) -> "State[T]":
        return self.with_variable(self[variable_name].assign(value))
