from abc import ABC, abstractmethod


class AbstractDelta(ABC):
    @abstractmethod
    def apply(self) -> None: ...

    @abstractmethod
    def revert(self) -> None: ...
