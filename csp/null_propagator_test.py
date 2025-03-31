from .delta_record import DeltaRecord
from .variable import Variable
from .state import State
from .domain import Domain
from .csp import CSP
from .null_propagator import NullPropagator


def test_null_propagator_success():
    delta_record = DeltaRecord()
    a = Variable(delta_record, "a", Domain(delta_record, {1, 2, 3}))
    state = State(delta_record, [a])
    csp = CSP([])

    propagator = NullPropagator()
    result = propagator.propagate(csp, state)

    assert result.success
    assert result.stats.domain_prunes == 0
    assert result.stats.constraint_checks == 0
