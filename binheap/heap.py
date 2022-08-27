import heapq
from typing import List


class Heap:
    def __init__(self, seq=()):
        self._heap: List = list(seq)
        heapq.heapify(self._heap)

    def __contains__(self, item):
        return item in self._heap

    def __delitem__(self, key):
        del self._heap[key]
        self.heapify()

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.to_list() == other.to_list()

    def __getitem__(self, item):
        return self._heap[item]

    def __iter__(self):
        return iter(self._heap)

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return str(self._heap)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._heap if self._heap else ""})'

    def clear(self):
        self._heap.clear()

    def heapify(self):
        return heapq.heapify(self._heap)

    def peek(self):
        """
        Returns the min/max element from the heap without actually
        removing it from the heap. Equivalent to heap[0].
        :return:
        """
        return self._heap[0]  # index out of range error

    def pop(self):
        """
        Removes and returns the min/max element from the heap.
        :return:
        """
        return heapq.heappop(self._heap)

    def push(self, items):
        """Push items onto the heap.

        - If `items` is an iterable then elements of the iterable are pushed
        individually.
        - If `items` isn't an iterable then it is pushed as a single item.
        :param items: Single item or an iterable
        :return:
        """
        try:
            for item in items:
                heapq.heappush(self._heap, item)
        except TypeError:
            heapq.heappush(self._heap, items)

    def push_pop(self, item):
        return heapq.heappushpop(self._heap, item)

    def replace(self, item):
        return heapq.heapreplace(self._heap, item)

    def to_list(self):
        """
        Returns heap elements as a new list.
        :return:
        """
        return list(self._heap)
