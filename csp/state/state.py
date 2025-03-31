from csp.state.variable import Variable
from csp.delta import DeltaObject, DeltaRecord
from typing import Iterable, Iterator, override
from collections.abc import Mapping


class State[T](DeltaObject, Mapping[str, Variable[T]]):
    class Error(Exception): ...

    class KeyError(Error, KeyError): ...

    def __init__(
        self,
        delta_record: DeltaRecord,
        variables: Iterable[Variable[T]],
    ) -> None:
        super().__init__(delta_record)
        if not all(
            variable._delta_record is self._delta_record for variable in variables
        ):
            raise self.Error("Delta record mismatch between variables and state")
        self._variables: dict[str, Variable[T]] = {v.name: v for v in variables}

    @override
    def __len__(self) -> int:
        return len(self._variables)

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._variables)

    @override
    def __getitem__(self, name: str) -> Variable[T]:
        try:
            return self._variables[name]
        except KeyError as e:
            raise self.KeyError(f"Variable {name} not found") from e

    def assign(self, name: str, value: T) -> None:
        self[name].assign(value)

    def unassign(self, name: str) -> None:
        self[name].unassign()

    def variables(self) -> Iterable[Variable[T]]:
        return self.values()

    def unassigned_variables(self) -> Iterable[Variable[T]]:
        return (v for v in self._variables.values() if not v.is_assigned())

    def is_valid(self) -> bool:
        return all(v.domain_size() > 0 for v in self._variables.values())
