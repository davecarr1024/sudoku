from .delta_object import DeltaObject
from .delta_record import DeltaRecord
from .delta import Delta
from typing import Optional, override
from .domain import Domain


class VariableAssign[T](Delta["Variable[T]"]):
    def __init__(self, obj: "Variable[T]", value: Optional[T]) -> None:
        super().__init__(obj)
        self._value = value
        self._previous = obj._value

    @override
    def apply(self) -> None:
        self._object._value = self._value

    @override
    def revert(self) -> None:
        self._object._value = self._previous


class Variable[T](DeltaObject):
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    class DomainError(Error): ...

    def __init__(
        self,
        delta_record: DeltaRecord,
        name: str,
        domain: Domain[T],
        value: Optional[T] = None,
    ) -> None:
        super().__init__(delta_record)
        self.name = name
        self.domain = domain
        if self._delta_record is not self.domain._delta_record:
            raise self.Error(
                f"Delta record mismatch between variable {self.name} and domain {self.domain}"
            )
        if value is not None and value not in self.domain:
            raise self.ValueError(f"Value {value} not in domain {self.domain}")
        self._value: Optional[T] = value

    def assign(self, value: Optional[T]) -> None:
        if value is not None and value not in self.domain:
            raise self.ValueError(f"{value} not in domain {self.domain}")
        self.apply(VariableAssign[T](self, value))

    def unassign(self) -> None:
        self.assign(None)

    def is_assigned(self) -> bool:
        return self._value is not None

    def value(self) -> Optional[T]:
        return self._value

    def add_value_to_domain(self, value: T) -> None:
        try:
            self.domain.add_value(value)
        except Domain.Error as e:
            raise self.DomainError("failed to add domain value {value}: {e}") from e

    def remove_value_from_domain(self, value: T) -> None:
        try:
            self.domain.remove_value(value)
        except Domain.Error as e:
            raise self.DomainError("failed to remove domain value {value}: {e}") from e

    def domain_values(self) -> set[T]:
        return set(self.domain)

    def domain_size(self) -> int:
        return len(self.domain)
