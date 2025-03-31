from csp.processing import Propagator
from csp.model import CSP
from csp.state import State


class NullPropagator[T](Propagator[T]):
    def propagate(self, csp: CSP[T], state: State[T]) -> Propagator.Result:
        """
        A propagator that performs no propagation.
        Always returns success=True with zero stats.
        """
        return Propagator.Result()
