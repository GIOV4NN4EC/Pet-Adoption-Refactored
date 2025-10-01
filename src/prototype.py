from abc import abstractmethod, ABC
from copy import deepcopy

class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass
