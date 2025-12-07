from typing import get_args
from strategy.input_bag_strategy.input_bag import InputBag
from strategy.novel_search_strategy.novel_search import NovelSearch
from strategy.random_strategy.random_strategy import RandomStrategy
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

    args = parser.parse_args()

    function: str = args.function
    strategy_name: StrategyEnum = args.strategy
    logdir: str = args.logdir

    strategy_type: type[Strategy]

    match strategy_name:
        case "input_bag":
            strategy_type = InputBag
        case "novelty_search":
            strategy_type = NovelSearch
        case "random":
            strategy_type = RandomStrategy

    strategy = strategy_type.with_branch_coverage({
        "name": function,
        "description": ""
    })
    strategy.run()
    

if __name__ == '__main__':
    main()
