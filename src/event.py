from datetime import date
from typing_extensions import override
from src.address import Address
from src.model import Model


class Event(Model):
    @classmethod
    def by_shelter(cls, shelter: str) -> list['Event']:
        return [ev for ev in cls.data.values() if ev.__shelter == shelter]

    @classmethod
    def actives(cls, shelter: str) -> list['Event']:
        return [ev for ev in cls.data.values() if ev.__status != "cancelled"]

    def __init__(self, name: str, event_date: date, location: Address, shelter: str):
        self.__name: str = name
        self.__date: date = event_date
        self.__address: Address = location
        self.__shelter: str = shelter
        self.__status: str = "planned"

        self.data[name] = self

    @property
    def name(self) -> str:
        return self.__name

    def cancel(self):
        self.__status = "cancelled"

    def complete(self):
        self.__status = "ended"

    @override
    def __str__(self) -> str:
        return f"{self.__name.upper()} by @{self.__shelter} in {self.__address.city}/{self.__address.state}"

    @override
    def formatted_list(self) -> list[str]:
        return [
            f"{self.__name.upper()} by @{self.__shelter}",
            f"   · [bold]Location:[/] {self.__address}",
            f"   · [bold]Date:[/] {self.__date.isoformat()}",
            f"   · [bold]Status:[/] {self.__status.upper()}"
        ]
