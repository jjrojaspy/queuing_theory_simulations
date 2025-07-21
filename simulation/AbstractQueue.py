from abc import ABC, abstractmethod


class AbstractQueue(ABC):
    @abstractmethod
    def add[T](self, customer: T):
        pass

    @abstractmethod
    def pop[T](self) -> T:
        pass

    @abstractmethod
    def capacity(self):
        pass

    @abstractmethod
    def count(self):
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass
