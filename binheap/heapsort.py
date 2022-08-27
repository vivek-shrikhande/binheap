from .minheap import MinHeap
from .maxheap import MaxHeap


def heapsort(iterable, reverse=False):
    heap = MaxHeap(iterable) if reverse else MinHeap(iterable)
    return [heap.pop() for _ in range(len(heap))]
