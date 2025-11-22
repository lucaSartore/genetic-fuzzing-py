from coverage_calc_lines import CoverageTester
from strategy.input_bag_strategy.input_bag import InputBag
from strategy.random_strategy.random_strategy import RandomStrategy


def main():
    strategy = InputBag.initialize({
    # strategy = RandomStrategy.initialize({
        # "name": "int_to_roman",
        # "name": "roman_to_int",
        # "name": "decode_string",
        # "name": "str_fun",
        # "name": "levenshtein_distance",
        "name": "count_bool",
        # "name": "is_valid_ip_address",
        "description": ""
    })
    strategy.run()
    

if __name__ == '__main__':
    main()
