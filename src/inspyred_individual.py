from typing import Protocol

class InspyredIndividual[T,S](Protocol):
    candidate: T
    fitness: S
