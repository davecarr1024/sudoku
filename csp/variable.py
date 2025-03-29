from dataclasses import dataclass, field
from typing import Optional, override
from functools import cache
from .domain import Domain


@dataclass(frozen=True)
class Variable[T]:
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    name: str
    domain: Domain[T]
    value: Optional[T] = None
    _cached_hash: int = field(
        init=False,
        repr=False,
        compare=False,
        hash=False,
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "_cached_hash",
            hash((self.name, self.domain, self.value)),
        )

    @override
    def __hash__(self) -> int:
        return self._cached_hash

    @staticmethod
    @cache
    def _make(name: str, domain: Domain[T], assigned: Optional[T]) -> "Variable[T]":
        return Variable[T](name, domain, assigned)

    @staticmethod
    def make(name: str, *values: T, assigned: Optional[T] = None) -> "Variable[T]":
        domain = Domain.for_values(*values)
        if assigned is not None and assigned not in domain:
            raise Variable[T].ValueError(f"value {assigned} is not in domain {domain}")
        return Variable[T]._make(name, domain, assigned)

    def assign(self, value: T) -> "Variable[T]":
        if value not in self.domain:
            raise self.ValueError(f"new value {value} is not in domain {self.domain}")
        return Variable[T].make(self.name, value, assigned=value)

    def with_domain(self, domain: Domain[T]) -> "Variable[T]":
        if self.value is not None and self.value not in domain:
            raise self.ValueError(f"value {self.value} is not in new domain {domain}")
        return Variable[T]._make(self.name, domain, self.value)

    def is_assigned(self) -> bool:
        return self.value is not None

    def is_valid(self) -> bool:
        return len(self.domain) > 0
