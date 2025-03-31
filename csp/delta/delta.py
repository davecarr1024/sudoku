from csp.delta.abstract_delta import AbstractDelta


class Delta[Object: "delta_object.DeltaObject"](AbstractDelta):
    def __init__(self, object: Object) -> None:
        self._object = object


from . import delta_object
