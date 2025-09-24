from abc import ABC, abstractmethod
from typing_extensions import Self

# ABSTRACT CLASS EXAMPLE


class Model(ABC):
    def __init_subclass__(cls):
        cls.data: dict[str, Self] = {}
        return super().__init_subclass__()

    @classmethod
    def __contains__(cls, item: str) -> bool:
        return item in cls.data.keys()

    @abstractmethod
    def formatted_list(self) -> list[str]:
        """returns all info in a formated list"""
        pass
