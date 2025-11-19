from typing import Self
from strategy.strategy import Strategy
from dataset.functions_list import FunctionType

class NovelSearchSettings():
    pass

class NovelSearch(Strategy[NovelSearchSettings]):
    @classmethod
    def initialize(cls, function: FunctionType, settings: NovelSearchSettings | None = None) -> Self:
        pass

    def run(self) -> list[tuple]:
        pass

