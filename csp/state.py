from .variable import Variable

from dataclasses import dataclass, field, replace
from typing import Iterator, Iterable, override, Self
from collections.abc import Mapping


@dataclass(frozen=True)
class State[T](Mapping[str, Variable[T]]):
    variables: Mapping[str, Variable[T]] = field(default_factory=dict)

    @override
    def __len__(self) -> int:
        return len(self.variables)

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self.variables)

    @override
    def __getitem__(self, key: str) -> Variable[T]:
        return self.variables[key]

    def _with_variables(self, variables: Mapping[str, Variable[T]]) -> Self:
        return replace(self, variables=variables)

    def with_variable(self, variable: Variable[T]) -> Self:
        return self._with_variables(dict(self.variables) | {variable.name: variable})

    def is_valid(self) -> bool:
        return all(var.is_valid() for var in self.variables.values())

    def unassigned_variables(self) -> Iterable[Variable[T]]:
        return (v for v in self.variables.values() if not v.is_assigned())

    def assign(self, variable_name: str, value: T) -> Self:
        return self.with_variable(self[variable_name].assign(value))
