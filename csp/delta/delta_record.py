from csp.delta.abstract_delta import AbstractDelta
from typing import override, Iterable, Sized, Iterator
from contextlib import contextmanager


class DeltaRecord(Sized, Iterable[AbstractDelta]):
    class Error(Exception): ...

    def __init__(self) -> None:
        self._deltas = list[AbstractDelta]()

    @override
    def __len__(self) -> int:
        return len(self._deltas)

    @override
    def __iter__(self) -> Iterator[AbstractDelta]:
        return iter(self._deltas)

    def apply(self, delta: AbstractDelta) -> None:
        delta.apply()
        self._deltas.append(delta)

    def revert(self) -> None:
        if not self._deltas:
            raise self.Error("No deltas to revert")
        delta = self._deltas.pop()
        delta.revert()

    def checkpoint(self) -> int:
        return len(self._deltas)

    def revert_to(self, checkpoint: int) -> None:
        while len(self._deltas) > checkpoint:
            self.revert()

    @contextmanager
    def maintain_state(self) -> Iterator[None]:
        checkpoint = self.checkpoint()
        try:
            yield
        finally:
            self.revert_to(checkpoint)
