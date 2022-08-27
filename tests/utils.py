import heapq
from random import randrange
from typing import Sequence, Union


def create_random_list(max_val, size):
    return [randrange(max_val) for _ in range(size)]


def create_heapq_heap(items):
    """Creates heap using heapq lib, heapify and returns it."""
    heapq_heap = list(items)
    heapq.heapify(heapq_heap)
    return heapq_heap


def negate(items: Union[Sequence, int]):
    """Recursively negates the items.

    This is used to emulate max heap using heapq lib.

    Examples:
    3 => -3
    [1, 2, 5] => [-1, -2, -5]
    [(1, 5), (8, 4)] => [(-1, -5), (-8, -4)]
    """
    try:
        return type(items)([negate(item) for item in items])
    except TypeError:
        return -items


def un_negate(items: Union[Sequence, int]):
    """Reverse the operation done by `negate` function.

    Examples:
    -3 => 3
    [-1, -2, -5] => [1, 2, 5]
    [(-1, -5), (-8, -4)] => [(1, 5), (8, 4)]
    """
    try:
        return type(items)([un_negate(item) for item in items])
    except TypeError:
        return -items
