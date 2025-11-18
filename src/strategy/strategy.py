from typing import Callable, Self
from abc import ABC, abstractmethod


class Strategy:
    @classmethod
    @abstractmethod
    def initialize(cls, function: Callable) -> Self:
        pass

    @abstractmethod
    def run(self) -> list[tuple]:
        pass

