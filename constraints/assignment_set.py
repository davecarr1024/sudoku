import dataclasses
from .assignment import Assignment
from typing import Self, Mapping, override, Iterator


@dataclasses.dataclass(frozen=True)
class AssignmentSet[T](Mapping[str, T]):
    assignments: frozenset[Assignment[T]] = dataclasses.field(default_factory=frozenset)

    @override
    def __len__(self) -> int:
        return len(self.assignments)

    @override
    def __iter__(self) -> Iterator[str]:
        for assignment in self.assignments:
            yield assignment.name

    @override
    def __getitem__(self, name: str) -> T:
        for assignment in self.assignments:
            if assignment.name == name:
                return assignment.value
        raise KeyError(name)

    def _with_assignments(self, assignments: frozenset[Assignment[T]]) -> Self:
        return dataclasses.replace(self, assignments=assignments)

    def with_assignment(self, assignment: Assignment[T]) -> Self:
        return self._with_assignments(
            assignments=self.assignments | frozenset({assignment})
        )

    def without_assignment(self, assignment: Assignment[T]) -> Self:
        return self._with_assignments(
            assignments=self.assignments - frozenset({assignment})
        )
