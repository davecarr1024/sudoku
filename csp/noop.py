from .abstract_delta import AbstractDelta
from typing import override


class Noop(AbstractDelta):
    @override
    def apply(self) -> None:
        pass

    @override
    def revert(self) -> None:
        pass
