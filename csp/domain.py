from dataclasses import dataclass, field
from typing import Iterator, override
from collections.abc import Set
from functools import cache


@dataclass(frozen=True)
class Domain[T](Set[T]):
    values: frozenset[T] = field(default_factory=frozenset)
    _cached_hash: int = field(
        init=False,
        repr=False,
        compare=False,
        hash=False,
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "_cached_hash", hash(self.values))

    @override
    def __hash__(self) -> int:
        return self._cached_hash

    @staticmethod
    @cache
    def _for_values(values: frozenset[T]) -> "Domain[T]":
        return Domain[T](values)

    @staticmethod
    def for_values(*values: T) -> "Domain[T]":
        return Domain[T]._for_values(frozenset(values))

    @override
    def __len__(self) -> int:
        return len(self.values)

    @override
    def __iter__(self) -> Iterator[T]:
        return iter(self.values)

    @override
    def __contains__(self, value: object) -> bool:
        return value in self.values

    def _with_values(self, values: frozenset[T]) -> "Domain[T]":
        return Domain[T]._for_values(values)

    def __and__(self, rhs: Set[T]) -> "Domain[T]":
        return self._with_values(self.values & frozenset(rhs))

    def __or__(self, rhs: Set[T]) -> "Domain[T]":
        return self._with_values(self.values | frozenset(rhs))

    def __sub__(self, rhs: Set[T]) -> "Domain[T]":
        return self._with_values(self.values - frozenset(rhs))

    def with_value(self, value: T) -> "Domain[T]":
        return self._with_values(self.values | frozenset({value}))

    def without_value(self, value: T) -> "Domain[T]":
        return self._with_values(self.values - frozenset({value}))
