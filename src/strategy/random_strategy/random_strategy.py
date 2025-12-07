from __future__ import annotations
from coverage_strategy import LineCoverageTester, BranchCoverageTester
from strategy.strategy import SettingsBaseClass, Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
import random
from strategy.input_bag_strategy.input_bag import Individual



@dataclass
class RandomStrategySettings(SettingsBaseClass):
    num_inputs: int = 50000

class RandomStrategy(Strategy[RandomStrategySettings]):
    def __init__(self, function: FunctionType, settings: RandomStrategySettings, log_dir: str):
        super().__init__(function, settings, log_dir)

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
