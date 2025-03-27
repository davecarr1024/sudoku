from dataclasses import dataclass, replace
from typing import Self, Optional
from .domain import Domain


@dataclass(frozen=True)
class Variable[T]:
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    name: str
    domain: Domain[T]
    value: Optional[T] = None

    @classmethod
    def make(cls, name: str, *values: T, assigned: Optional[T] = None) -> Self:
        domain = Domain.for_values(*values)
        if assigned is not None and assigned not in domain:
            raise cls.ValueError(f"value {assigned} is not in domain {domain}")
        return cls(name, domain, assigned)

    def assign(self, value: T) -> Self:
        if value not in self.domain:
            raise self.ValueError(f"new value {value} is not in domain {self.domain}")
        return replace(self, value=value, domain=Domain[T].for_values(value))

    def with_domain(self, domain: Domain[T]) -> Self:
        if self.value is not None and self.value not in domain:
            raise self.ValueError(f"value {self.value} is not in new domain {domain}")
        return replace(self, domain=domain)

    def is_assigned(self) -> bool:
        return self.value is not None

    def is_valid(self) -> bool:
        return len(self.domain) > 0
