from typing import Protocol

class InspyredIndividual[T](Protocol):
    candidate: T
    fitness: float
