from typing_extensions import override


class Address:
    def __init__(self, street: str, district: str, number: str,
                 postal_code: int, city: str, state: str):
        self.__street: str = street
        self.__district: str = district
        self.__number: str = number
        self.__postal_code: int = postal_code
        self.__city: str = city
        self.__state: str = state

    @property
    def city(self) -> str:
        return self.__city

    @property
    def state(self) -> str:
        return self.__state

    @override
    def __str__(self) -> str:
        return (f"{self.__street}, {self.__number}, {self.__district} - "
                + f"{self.__city}/{self.__state}")
