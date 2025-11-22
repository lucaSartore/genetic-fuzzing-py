from strategy.input_bag_strategy.input_bag import InputBag


def main():
    strategy = InputBag.initialize({
        "name": "int_to_roman",
        "description": ""
    })
    strategy.run()
    

if __name__ == '__main__':
    main()
