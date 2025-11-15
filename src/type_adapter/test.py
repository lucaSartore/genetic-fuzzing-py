

from type_adapter.args_dispatcher import ArgsDispatcher


def fn(a: int, b: bool, c: list[int], d: list[bool], e: list[list[int]]):
    print(a,b,c,d,e)


def test_args_dispatcher():
    ad = ArgsDispatcher.initialize(fn)
    ad.mutate()
    args = ad.get_args()
    fn(*args)
    

