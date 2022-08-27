import heapq
from random import randint

from pytest import raises

from binheap import MinHeap, MaxHeap
from .utils import create_heapq_heap, create_random_list


class DummyObject:
    def __init__(self, val):
        self.val = val


class TestMinHeap:
    MAX_VAL, SIZE = 100, 10

    def test_init(self):
        # empty heap
        min_heap = MinHeap()
        assert min_heap.to_list() == []

        # init with list items
        items = [7, 1, 5, 4, 6, 3]
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)
        assert min_heap.to_list() == heapq_heap

        # init with tuple items
        items = (7, 1, 5, 4, 6, 3)
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)
        assert min_heap.to_list() == heapq_heap

        # init with tuple of tuples
        items = ((7, 1), (5, 4), (6, 3))
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)
        assert min_heap.to_list() == heapq_heap

    def test_heapify(self):
        # todo: when support to key parameter is added.
        pass

    def test_peek(self):
        # peek on empty heap
        with raises(IndexError):
            MinHeap().peek()

        # peek on non-empty heap
        items = ((7, 1), (5, 4), (6, 3))
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)
        assert min_heap.pop() == heapq_heap[0]

    def test_pop(self):
        # pop on empty heap
        with raises(IndexError):
            MinHeap().pop()

        # pop on non-empty heap
        items = ((7, 1), (5, 4), (6, 3))
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)
        assert min_heap.pop() == heapq.heappop(heapq_heap)

    def test_push(self):
        # single item
        item = 1
        min_heap, heapq_heap = MinHeap(), list()
        min_heap.push(item)
        heapq.heappush(heapq_heap, item)
        assert min_heap.to_list() == heapq_heap

        # many items
        items = [7, 1, 5, 4, 6, 3]
        min_heap, heapq_heap = MinHeap(), list()
        min_heap.push(items)
        for item in items:
            heapq.heappush(heapq_heap, item)
        assert min_heap.to_list() == heapq_heap

        # tuple of tuples
        items = ((7, 1), (5, 4), (6, 3))
        min_heap, heapq_heap = MinHeap(), list()
        min_heap.push(items)
        for item in items:
            heapq.heappush(heapq_heap, item)
        assert min_heap.pop() == heapq.heappop(heapq_heap)

    def test_push_pop(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)

        # element that doesn't exist and min of all the items
        new_item = min(items) - 1
        assert min_heap.push_pop(new_item) == heapq.heappushpop(heapq_heap, new_item)

        # element that doesn't exist but not min
        min_item = min(items)
        for new_item in range(min_item + 1, self.MAX_VAL):
            if new_item in items:
                continue

            assert min_heap.push_pop(new_item) == heapq.heappushpop(heapq_heap, new_item)
            break

        # element that already exist and min
        new_item = min(items)
        assert min_heap.push_pop(new_item) == heapq.heappushpop(heapq_heap, new_item)

        # element that already exist and not min
        new_item = sorted(items)[1]
        assert min_heap.push_pop(new_item) == heapq.heappushpop(heapq_heap, new_item)

    def test_to_list(self):
        assert MinHeap().to_list() == []

        # init with tuple
        assert MinHeap((5, 1)).to_list() == [1, 5]

        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)
        assert min_heap.to_list() == heapq_heap

    def test_replace(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)

        # element that doesn't exist and min
        new_item = min(items) - 1
        assert min_heap.replace(new_item) == heapq.heapreplace(heapq_heap, new_item)

        # element that doesn't exist and not min
        min_item = min(items)
        for new_item in range(min_item + 1, self.MAX_VAL):
            if new_item in items:
                continue

            assert min_heap.replace(new_item) == heapq.heapreplace(heapq_heap, new_item)
            break

        # element that already exist and min
        new_item = min(items)
        assert min_heap.replace(new_item) == heapq.heapreplace(heapq_heap, new_item)

        # element that already exist and not min
        new_item = sorted(items)[1]
        assert min_heap.replace(new_item) == heapq.heapreplace(heapq_heap, new_item)

    def test_clear(self):
        min_heap = MinHeap(create_random_list(self.MAX_VAL, self.SIZE))
        min_heap.clear()
        assert len(min_heap) == 0

    # heapify and push don't produce the same order of elements
    def test_eq(self):
        min_heap = MinHeap()
        assert min_heap == MinHeap()

        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap = MinHeap(items)
        assert min_heap == MinHeap(items)

        # different len
        assert min_heap != MinHeap(items + [10])

        # different type
        assert MinHeap() != MaxHeap()

        # list is not the same as Heap even though the elements and the order is the same.
        assert min_heap.to_list() != MinHeap(items)

    def test_contains(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap = MinHeap(items)
        assert items[0] in min_heap

        assert (-1 in min_heap) is False

    def test_delitem(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)

        del min_heap[0]
        del heapq_heap[0]
        heapq.heapify(heapq_heap)

        assert min_heap.to_list() == heapq_heap

    def test_iter(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap, heapq_heap = MinHeap(items), create_heapq_heap(items)

        for i, item in enumerate(min_heap):
            assert item == heapq_heap[i]

    def test_getitem(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap = MinHeap(items)

        # positive index
        index = randint(0, self.SIZE - 1)
        assert min_heap[index] == min_heap.to_list()[index]

        # negative index
        index = randint(-self.SIZE, -1)
        assert min_heap[index] == min_heap.to_list()[index]

        # slice
        start = randint(0, self.SIZE - 1)
        end = randint(start, self.SIZE)
        assert min_heap[start:end] == min_heap.to_list()[start:end]

    def test_len(self):
        assert len(MinHeap()) == 0

        items = create_random_list(self.MAX_VAL, self.SIZE)
        assert len(MinHeap(items)) == len(items)

    def test_str(self):
        assert str(MinHeap()) == '[]'

        items = create_random_list(self.MAX_VAL, self.SIZE)
        min_heap = MinHeap(items)
        assert str(min_heap) == str(min_heap.to_list())

    def test_repr(self):
        assert repr(MinHeap()) == 'MinHeap()'

        min_heap = MinHeap(create_random_list(self.MAX_VAL, self.SIZE))
        assert repr(min_heap) == f'MinHeap({min_heap.to_list()})'
