from type_adapter.args_dispatcher import ArgsDispatcher
from random import Random


def fn(a: int, b: bool, c: list[int], d: list[bool], e: list[dict[int, bool]]):
    print('############ ARGS ##############')
    print(a,b,c,d,e)


def test_args_dispatcher():
    rand = Random()
    ad = ArgsDispatcher.initialize(rand, fn)
    for _ in range(100): 
        ad.mutate(rand)
        args = ad.get_args()
        fn(*args)
    

