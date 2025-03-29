from .delta import Delta
from .delta_object import DeltaObject
from .delta_record import DeltaRecord
from .noop import Noop
from typing import override, Iterator
from collections.abc import Set


class DomainAddValue[T](Delta["Domain[T]"]):
    def __init__(self, object: "Domain[T]", value: T) -> None:
        super().__init__(object)
        self._value = value

    @override
    def apply(self) -> None:
        self._object._add_value(self._value)

    @override
    def revert(self) -> None:
        self._object._remove_value(self._value)


class DomainRemoveValue[T](Delta["Domain[T]"]):
    def __init__(self, object: "Domain[T]", value: T) -> None:
        super().__init__(object)
        self._value = value

    @override
    def apply(self) -> None:
        self._object._remove_value(self._value)

    @override
    def revert(self) -> None:
        self._object._add_value(self._value)


class Domain[T](DeltaObject, Set[T]):
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __init__(
        self,
        delta_record: DeltaRecord,
        values: set[T],
    ) -> None:
        super().__init__(delta_record)
        self._values = set(values)

    @override
    def __contains__(self, value: object) -> bool:
        return value in self._values

    @override
    def __iter__(self) -> Iterator[T]:
        return iter(self._values)

    @override
    def __len__(self) -> int:
        return len(self._values)

    @override
    def __str__(self) -> str:
        return f"Domain({self._values})"

    def add_value(self, value: T) -> None:
        if value in self:
            self.apply(Noop())
        else:
            self.apply(DomainAddValue[T](self, value))

    def _add_value(self, value: T) -> None:
        self._values.add(value)

    def remove_value(self, value: T) -> None:
        if value not in self:
            raise self.ValueError(f"Value {value} not in domain {self}")
        self.apply(DomainRemoveValue[T](self, value))

    def _remove_value(self, value: T) -> None:
        self._values.remove(value)
