from typing import Callable, Self
from strategy.strategy import Strategy


class NovelSearch(Strategy):
    @classmethod
    def initialize(cls, function: Callable) -> Self:
        pass

    def run(self) -> list[tuple]:
        pass

