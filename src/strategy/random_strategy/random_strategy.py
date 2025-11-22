from __future__ import annotations
from typing import Self
from coverage_calc_lines import CoverageTester
from strategy.strategy import Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
import random
from strategy.input_bag_strategy.input_bag import Individual



@dataclass
class RandomStrategySettings():
    num_inputs: int = 5000

class RandomStrategy(Strategy[RandomStrategySettings]):
    @classmethod
    def initialize(cls, function: FunctionType, settings: RandomStrategySettings | None = None) -> Self:
        if settings is None:
            settings = RandomStrategySettings()
        return cls(function, settings)

    def __init__(self, function: FunctionType, settings: RandomStrategySettings):
        self.tester = CoverageTester(function)
        self.function = self.tester.export_fn
        self.settings = settings

    def run(self) -> list[tuple]:
        rand = random.Random()
        rand.seed(2347)

        individual = Individual([
            ArgsDispatcher.initialize(random, self.function)
            for _ in range(self.settings.num_inputs)
        ])

        score = individual.evaluate(self.tester)

        print(f"best score = {score}")
        args = individual.get_args()
        # print(f"args = {args}")
        return args
