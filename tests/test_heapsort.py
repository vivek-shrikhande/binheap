from random import randrange

from binheap import heapsort


class TestHeapSort:

    def test_heapsort(self):
        items = [randrange(100) for _ in range(100)]

        # ascending sort
        assert heapsort(items) == sorted(items)

        # descending sort
        assert heapsort(items, reverse=True) == sorted(items, reverse=True)
