import heapq
from random import randint

from pytest import raises

from binheap import MaxHeap, MinHeap
from .utils import create_heapq_heap, create_random_list, negate, un_negate


class TestMaxHeap:
    MAX_VAL, SIZE = 100, 10

    def test_init(self):
        # empty heap
        max_heap = MaxHeap()
        assert max_heap.to_list() == []

        # init with list items
        items = [7, 1, 5, 4, 6, 3]
        max_heap = MaxHeap(items)
        # negate items to emulate max heap through the heapq library
        heapq_heap = create_heapq_heap(negate(items))
        assert max_heap.to_list() == un_negate(heapq_heap)

        # init with tuple items
        items = (7, 1, 5, 4, 6, 3)
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))
        assert max_heap.to_list() == un_negate(heapq_heap)

        # init with tuple of tuples
        items = ((7, 1), (5, 4), (6, 3))
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))
        assert max_heap.to_list() == un_negate(heapq_heap)

    def test_heapify(self):
        # todo: when support to key parameter is added.
        pass

    def test_peek(self):
        # peek on empty heap
        with raises(IndexError):
            MaxHeap().peek()

        # peek on non-empty heap
        items = ((5, 4), (7, 1), (6, 3))
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))
        assert max_heap.peek() == un_negate(heapq_heap[0])

    def test_pop(self):
        # pop on empty heap
        with raises(IndexError):
            MaxHeap().pop()

        # pop on non-empty heap
        items = ((7, 1), (5, 4), (6, 3))
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))
        assert max_heap.pop() == un_negate(heapq.heappop(heapq_heap))

    def test_push(self):
        # single item
        item = 1
        max_heap, heapq_heap = MaxHeap(), list()
        max_heap.push(item)
        heapq.heappush(heapq_heap, item)
        assert max_heap.to_list() == heapq_heap

        # many items
        items = [7, 1, 5, 4, 6, 3]
        max_heap, heapq_heap = MaxHeap(), list()
        max_heap.push(items)
        for item in items:
            heapq.heappush(heapq_heap, -item)
        assert max_heap.to_list() == un_negate(heapq_heap)

        # tuple of tuples
        items = ((7, 1), (5, 4), (6, 3))
        max_heap, heapq_heap = MaxHeap(), list()
        max_heap.push(items)
        for item in items:
            heapq.heappush(heapq_heap, tuple(-val for val in item))
        assert max_heap.pop() == un_negate(heapq.heappop(heapq_heap))

    def test_push_pop(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))

        # element that doesn't exist and min of all the items
        new_item = min(items) - 1
        assert max_heap.push_pop(new_item) == un_negate(heapq.heappushpop(heapq_heap, new_item))

        # element that doesn't exist but not min
        min_item = min(items)
        for new_item in range(min_item + 1, self.MAX_VAL):
            if new_item in items:
                continue

            assert max_heap.push_pop(new_item) == un_negate(heapq.heappushpop(heapq_heap, new_item))
            break

        # element that already exist and min
        new_item = min(items)
        assert max_heap.push_pop(new_item) == un_negate(heapq.heappushpop(heapq_heap, new_item))

        # element that already exist and not min
        new_item = sorted(items)[1]
        assert max_heap.push_pop(new_item) == un_negate(heapq.heappushpop(heapq_heap, new_item))

    def test_to_list(self):
        assert MaxHeap().to_list() == []

        # init with tuple
        assert MaxHeap((5, 1)).to_list() == [5, 1]

        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))
        assert max_heap.to_list() == un_negate(heapq_heap)

    def test_replace(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))

        # element that doesn't exist and min
        new_item = min(items) - 1
        assert max_heap.replace(new_item) == un_negate(heapq.heapreplace(heapq_heap, new_item))

        # element that doesn't exist and not min
        min_item = min(items)
        for new_item in range(min_item + 1, self.MAX_VAL):
            if new_item in items:
                continue

            assert max_heap.replace(new_item) == un_negate(heapq.heapreplace(heapq_heap, new_item))
            break

        # element that already exist and min
        new_item = min(items)
        assert max_heap.replace(new_item) == un_negate(heapq.heapreplace(heapq_heap, new_item))

        # element that already exist and not min
        new_item = sorted(items)[1]
        assert max_heap.replace(new_item) == un_negate(heapq.heapreplace(heapq_heap, new_item))

    def test_clear(self):
        max_heap = MaxHeap(create_random_list(self.MAX_VAL, self.SIZE))
        max_heap.clear()
        assert len(max_heap) == 0

    # heapify and push don't produce the same order of elements
    def test_eq(self):
        max_heap = MaxHeap()
        assert max_heap == MaxHeap()

        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap = MaxHeap(items)
        assert max_heap == MaxHeap(items)

        # different len
        assert max_heap != MaxHeap(items + [10])

        # different type
        assert MaxHeap() != MinHeap()

        # list is not the same as Heap even though the elements and the order is the same.
        assert max_heap.to_list() != MaxHeap(items)

    def test_contains(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap = MaxHeap(items)

        # contains
        assert items[0] in max_heap

        # doesn't contain
        assert (-1 in max_heap) is False

    def test_delitem(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))

        del max_heap[0]
        del heapq_heap[0]
        heapq.heapify(heapq_heap)

        assert max_heap.to_list() == un_negate(heapq_heap)

    def test_iter(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap, heapq_heap = MaxHeap(items), create_heapq_heap(negate(items))

        for i, item in enumerate(max_heap):
            assert item == un_negate(heapq_heap[i])

    def test_getitem(self):
        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap = MaxHeap(items)

        # positive index
        index = randint(0, self.SIZE - 1)
        assert max_heap[index] == max_heap.to_list()[index]

        # negative index
        index = randint(-self.SIZE, -1)
        assert max_heap[index] == max_heap.to_list()[index]

        # slice
        start = randint(0, self.SIZE - 1)
        end = randint(start, self.SIZE)
        assert max_heap[start:end] == max_heap.to_list()[start:end]

    def test_len(self):
        assert len(MaxHeap()) == 0

        items = create_random_list(self.MAX_VAL, self.SIZE)
        assert len(MaxHeap(items)) == len(items)

    def test_str(self):
        assert str(MaxHeap()) == '[]'

        items = create_random_list(self.MAX_VAL, self.SIZE)
        max_heap = MaxHeap(items)
        assert str(max_heap) == str(max_heap.to_list())

    def test_repr(self):
        assert repr(MaxHeap()) == 'MaxHeap()'

        max_heap = MaxHeap(create_random_list(self.MAX_VAL, self.SIZE))
        assert repr(max_heap) == f'MaxHeap({max_heap.to_list()})'
