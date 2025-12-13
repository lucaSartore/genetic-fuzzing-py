from __future__ import annotations
from coverage_strategy import LineCoverageTester, BranchCoverageTester
from coverage_strategy.coverage import ExecutionResult
from strategy.strategy import SettingsBaseClass, Strategy
from dataclasses import dataclass
from dataset.functions_list import FunctionType
from type_adapter.args_dispatcher import ArgsDispatcher
import random
from random import Random
from strategy.input_bag_strategy.input_bag import Individual


# equal time spent
@dataclass
# class RandomStrategySettings(SettingsBaseClass):
#     num_generations: int = 7250
#     num_individuals = 500

# equal number of function calls
# @dataclass
class RandomStrategySettings(SettingsBaseClass):
    num_generations: int = 10
    num_individuals: int = 500

class RandomStrategy(Strategy[RandomStrategySettings]):
    @classmethod
    def default_settings(cls) -> RandomStrategySettings:
        return RandomStrategySettings()

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

        def exp_mutation(random: Random, dispatcher: ArgsDispatcher):
            if random.random() > 0.5:
                dispatcher.mutate(random)
                return exp_mutation(random, dispatcher)
            return dispatcher

        result: ExecutionResult | None = None

        for _ in range(self.settings.num_generations):

            individual = Individual([
                exp_mutation(rand, ArgsDispatcher.initialize(rand, self.function))
                for _ in range(self.settings.num_individuals)
            ])

            new_result = individual.get_test_result(self.tester)

            if result == None:
                result = new_result
            else:
                result = result.merge_one(new_result)

            score = result.fraction_covered()
            self.log(score)

        return []
