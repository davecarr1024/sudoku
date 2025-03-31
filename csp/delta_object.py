from .delta_record import DeltaRecord
from .abstract_delta import AbstractDelta
from contextlib import contextmanager
from typing import Iterator


class DeltaObject:
    def __init__(self, delta_record: DeltaRecord) -> None:
        self._delta_record = delta_record

    def apply(self, delta: AbstractDelta) -> None:
        self._delta_record.apply(delta)

    def revert(self) -> None:
        self._delta_record.revert()

    @contextmanager
    def maintain_state(self) -> Iterator[None]:
        with self._delta_record.maintain_state():
            yield

    def checkpoint(self) -> int:
        return self._delta_record.checkpoint()

    def revert_to(self, checkpoint: int) -> None:
        self._delta_record.revert_to(checkpoint)
