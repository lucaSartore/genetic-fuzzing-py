from __future__ import annotations
from typing import Self, Type
from coverage_strategy import CoverageTester, LineCoverageTester, BranchCoverageTester
from strategy.strategy import Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
import random
from strategy.input_bag_strategy.input_bag import Individual



@dataclass
class RandomStrategySettings():
    num_inputs: int = 50000
    coverage_tester_class: Type[CoverageTester] = LineCoverageTester

class RandomStrategy(Strategy[RandomStrategySettings]):
    @classmethod
    def initialize(cls, function: FunctionType, settings: RandomStrategySettings | None = None) -> Self:
        if settings is None:
            settings = RandomStrategySettings()
        return cls(function, settings)

    @classmethod
    def with_line_coverage(cls, function: FunctionType, settings: RandomStrategySettings | None = None) -> Self:
        """Create RandomStrategy with line coverage tester."""
        if settings is None:
            settings = RandomStrategySettings()
        settings.coverage_tester_class = LineCoverageTester
        return cls(function, settings)
    
    @classmethod 
    def with_branch_coverage(cls, function: FunctionType, settings: RandomStrategySettings | None = None) -> Self:
        """Create RandomStrategy with branch coverage tester."""
        if settings is None:
            settings = RandomStrategySettings()
        settings.coverage_tester_class = BranchCoverageTester
        return cls(function, settings)

    def __init__(self, function: FunctionType, settings: RandomStrategySettings):
        self.tester = settings.coverage_tester_class(function)
        self.function = self.tester.export_fn
        self.settings = settings
        self.function_def = function  # Store original function definition for switching

    def set_coverage_type(self, coverage_type: str) -> None:
        """Switch between different coverage types."""
        if coverage_type == "line":
            self.settings.coverage_tester_class = LineCoverageTester
        elif coverage_type == "branch":
            self.settings.coverage_tester_class = BranchCoverageTester
        else:
            raise ValueError(f"Unknown coverage type: {coverage_type}. Use 'line' or 'branch'.")
        
        # Recreate the tester with the new coverage type
        self.tester = self.settings.coverage_tester_class(self.function_def)
        self.function = self.tester.export_fn

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
