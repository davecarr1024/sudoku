from dataclasses import dataclass, field, replace
from typing import Iterator, override, Self
from collections.abc import Set


@dataclass(frozen=True)
class Domain[T](Set[T]):
    values: frozenset[T] = field(default_factory=frozenset)

    @classmethod
    def for_values(cls, *values: T) -> Self:
        return cls(frozenset(values))

    @override
    def __len__(self) -> int:
        return len(self.values)

    @override
    def __iter__(self) -> Iterator[T]:
        return iter(self.values)

    @override
    def __contains__(self, value: T) -> bool:
        return value in self.values

    def _with_values(self, values: frozenset[T]) -> Self:
        return replace(self, values=values)

    def __and__(self, rhs: Self) -> Self:
        return self._with_values(self.values & rhs.values)

    def __or__(self, rhs: Self) -> Self:
        return self._with_values(self.values | rhs.values)

    def __sub__(self, rhs: Self) -> Self:
        return self._with_values(self.values - rhs.values)

    def with_value(self, value: T) -> Self:
        return self._with_values(self.values | frozenset({value}))

    def without_value(self, value: T) -> Self:
        return self._with_values(self.values - frozenset({value}))
