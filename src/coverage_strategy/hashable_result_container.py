from functools import reduce
from typing import Hashable


class HashableResultContainer[T: Hashable]:
    def __init__(self, included: list[T], excluded: list[T]):
        self.included = included
        self.excluded = excluded
        self._hash: int | None = None

    def list_equal(self, l1: list[T], l2: list[T]) -> bool:
        return reduce(
            lambda r,v: r and v[0] == v[1],
            zip(l1, l2),
            True
        )


    def __eq__(self, value: object, /) -> bool:
        if (type(value) != HashableResultContainer):
            return False

        if len(self.included) != len(value.included) or \
            len(self.excluded) != len(value.excluded):
            return False

        v1 = self.list_equal(self.included, value.included)
        v2 = self.list_equal(self.excluded, value.excluded)

        return self.list_equal(self.included, value.included) and \
        self.list_equal(self.excluded, value.excluded)

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash=  hash((
                tuple(self.included),
                tuple(self.excluded)
            ))
        
        return self._hash
        

