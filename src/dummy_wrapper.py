from typing import Literal, get_args
from coverage_strategy.branch_coverage import BranchCoverageTester
from coverage_strategy.line_coverage import LineCoverageTester
from strategy.input_bag_strategy.input_bag import InputBag, InputBagSettings
from strategy.novel_search_strategy.novel_search import NovelSearch, NovelSearchSettings
from strategy.random_strategy.random_strategy import RandomStrategy, RandomStrategySettings
import argparse

from strategy.strategy import Strategy, StrategyEnum


def main():

    parser = argparse.ArgumentParser(
                    prog='DummyWrapper',
                    description='execute one function')

    parser.add_argument("-f", "--function", default="count_bool")
    parser.add_argument(
        "-s", "--strategy",
        default="random",
        choices=list(get_args(StrategyEnum))
    )

    parser.add_argument("-l", "--logdir", default="X")
    parser.add_argument("-c", "--coverage", default="branch", choices=["branch","line"])
    parser.add_argument("-p", "--parity", default="function_call", choices=["function_call","time"])

    args = parser.parse_args()

    function: str = args.function
    strategy_name: StrategyEnum = args.strategy
    logdir: str = args.logdir
    coverage: Literal["branch","line"] = args.coverage
    parity: Literal["function_call", "time"] = args.parity

    strategy_type: type[Strategy]
    
    match (strategy_name, parity):
        case ("novelty_search", _):
            settings = NovelSearchSettings(
                num_individuals= 1,
                num_generations= 10_000,
                num_selected= 1
            )

        case ("input_bag", "time"):
            settings = InputBagSettings(
                num_inputs= 100,
                num_individuals= 50,
                num_generations= 800,
                num_selected= 10
            )
        case ("input_bag", "function_call"):
            settings = InputBagSettings(
                num_inputs= 20,
                num_individuals= 20,
                num_generations= 25,
                num_selected= 10
            )
        case ("random", "time"):
            settings = RandomStrategySettings(
                num_generations= 7250,
                num_individuals= 500
            )
        case ("random", "function_call"):
            settings = RandomStrategySettings(
                num_generations= 20,
                num_individuals= 500
            )
    if coverage == "branch":
        settings.coverage_tester_class = BranchCoverageTester
    else:
        settings.coverage_tester_class = LineCoverageTester

    match strategy_name:
        case "input_bag":
            strategy_type = InputBag
        case "novelty_search":
            strategy_type = NovelSearch
        case "random":
            strategy_type = RandomStrategy

    strategy = strategy_type.initialize({
        "name": function,
        "description": ""
    }, settings, logdir) #type: ignore
    strategy.run()
    

if __name__ == '__main__':
    main()
