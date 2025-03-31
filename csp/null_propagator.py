from .propagator import Propagator
from .csp import CSP
from .state import State


class NullPropagator[T](Propagator[T]):
    def propagate(self, csp: CSP[T], state: State[T]) -> Propagator.Result:
        """
        A propagator that performs no propagation.
        Always returns success=True with zero stats.
        """
        return Propagator.Result()
