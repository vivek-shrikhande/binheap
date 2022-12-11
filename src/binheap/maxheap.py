from __future__ import annotations

from typing import Any

from .heap import Heap


class Inverted:
    __slots__ = ('_val',)

    def __init__(self, val: Any):
        self._val = val

    def __eq__(self, other: Inverted):
        return self.__class__ == other.__class__ and self._val == other._val

    def __lt__(self, other: Inverted):
        """
        IMP: <=
        :param other:
        :return:
        """
        # return not self.val <= other.val
        return other._val < self._val

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return repr(self._val)

    def val(self):
        return self._val


def invert(val: Any) -> Inverted:
    return Inverted(val)


def uninvert(obj: Inverted) -> Any:
    return obj.val()


class MaxHeap(Heap):
    def __init__(self, seq=()):
        super().__init__(invert(item) for item in seq)

    def __contains__(self, item):
        return invert(item) in self._heap

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [uninvert(item) for item in self._heap[item]]
        return uninvert(self._heap[item])

    def __iter__(self):
        return (uninvert(item) for item in self._heap)

    def peek(self):
        return uninvert(super().peek())

    def pop(self):
        return uninvert(super().pop())

    def push(self, items):
        try:
            super().push(invert(item) for item in items)
        except TypeError:
            super().push(invert(items))

    def push_pop(self, item):
        return uninvert(super().push_pop(invert(item)))

    def replace(self, item):
        return uninvert(super().replace(invert(item)))

    def to_list(self):
        return [uninvert(item) for item in super().to_list()]
