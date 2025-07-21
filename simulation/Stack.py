import numpy as np

from simulation.AbstractQueue import AbstractQueue


class Stack[T](AbstractQueue):
    def __init__(self, capacity, dtype=T):
        self._capacity = capacity
        self._count = 0

        self.array = np.empty(capacity, dtype=dtype)
        self.top = -1

    def add(self, customer: T):
        if self.top == self._capacity - 1:
            raise OverflowError("Full capacity reached: no more customers can be received!")

        self._count += 1
        self.top += 1
        self.array[self.top] = customer

    def pop(self) -> T:
        if self.top == -1:
            raise IndexError("No more customers have arrived!")

        customer = self.array[self.top]
        self.top -= 1
        self._count -= 1

        return customer

    def capacity(self):
        return self._capacity

    def count(self):
        return self._count

    def is_empty(self) -> bool:
        return self._count == 0
