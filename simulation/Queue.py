import numpy as np

from simulation.AbstractQueue import AbstractQueue


class Queue[T](AbstractQueue):
    def __init__(self, capacity, dtype=T):
        self._capacity = capacity
        self._count = 0

        self.array = np.empty(capacity, dtype=dtype)
        self.head = 0
        self.tail = 0

    def add(self, customer: T):
        self.array[self.tail] = customer
        self.tail = (self.tail + 1) % self._capacity
        if self._count < self._capacity:
            self._count += 1
        else:
            raise OverflowError("Full capacity reached: no more customers can be received!")

    def pop(self) -> T:
        if self._count == 0:
            raise IndexError("No more customers have arrived!")

        customer = self.array[self.head]
        self.head = (self.head + 1) % self._capacity
        self._count -= 1

        return customer

    def capacity(self) -> int:
        return self._capacity

    def count(self) -> int:
        return self._count

    def is_empty(self) -> bool:
        return self._count == 0
