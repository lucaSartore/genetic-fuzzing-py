from strategy.input_bag_strategy.input_bag import InputBag
from strategy.novel_search_strategy.novel_search import NovelSearch
from strategy.random_strategy.random_strategy import RandomStrategy
import sys


def main():
    
    strategy = NovelSearch.with_branch_coverage({
    # strategy = NovelSearch.initialize({
    # strategy = RandomStrategy.initialize({
        #"name": "int_to_roman",
        # "name": "roman_to_int",
        # "name": "decode_string",
        # "name": "str_fun",
        # "name": "levenshtein_distance",
         "name": sys.argv[1],
        # "name": "is_odd_for_dummys",
        # "name": "is_valid_ip_address",
        "description": ""
    })
    strategy.run()
    

if __name__ == '__main__':
    main()