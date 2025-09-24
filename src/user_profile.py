from datetime import date
from dateutil import relativedelta
from typing_extensions import override

from .address import Address

# ENCAPSULATION EXAMPLE


class Profile:
    def __init__(self, name: str, birth: date | None = None,
                 address: Address | None = None,
                 desc: str | None = None):
        self.__name: str = name
        self.__birth: date | None = birth
        self.__address: Address | None = address
        self.__description: str | None = desc

    def dictionary(self) -> dict[str, int | str | None]:
        return {
            "name": self.name,
            "age": self.age,
            "city": self.city,
            "state": self.state
        }

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_name: str):
        if len(new_name) > 0:
            self.__name = new_name

    @property
    def birth(self) -> str | None:
        """returns None if no birth was added to profile"""

        if self.__birth:
            return self.__birth.isoformat()
        return None

    @property
    def age(self) -> int | None:
        """returns None if no birth was added to profile"""

        if self.__birth:
            return relativedelta.relativedelta(date.today(), self.__birth).years
        return None

    @birth.setter
    def birth(self, new_birth: date):
        if isinstance(new_birth, date) and new_birth <= date.today():
            self.__birth = new_birth

    @property
    def address(self) -> Address | None:
        """returns None if no address was added to profile"""

        if self.__address:
            return self.__address

        return None

    @address.setter
    def address(self, new_address: Address):
        if isinstance(new_address, Address):
            self.__address = new_address

    @property
    def city(self) -> str | None:
        """returns None if no address was added to profile"""

        if self.__address:
            return self.__address.city

        return None

    @property
    def state(self) -> str | None:
        """returns None if no address was added to profile"""

        if self.__address:
            return self.__address.state

        return None

    @property
    def description(self) -> str | None:
        """returns None if no description was added to profile"""

        return self.__description

    @description.setter
    def description(self, new_desc: str):
        if len(new_desc) > 0:
            self.__description = new_desc

    def as_list(self) -> list[str]:
        info: list[str] = [self.__name]

        if self.__birth:
            info.append(self.__birth.isoformat())

        if self.__address:
            info.append(self.__address.__str__())

        if self.__description:
            info.append(self.__description)

        return info

    def formatted_list(self) -> list[str]:
        profile_info: list[str] = [f"\n{self.__name.upper()}"]

        if self.__birth:
            profile_info.append(f"    > [bold]Age:[/] {self.age}")

        if self.__address:
            profile_info.append(f"    > [bold]Address:[/] {self.__address}")

        if self.__description:
            profile_info.append(
                f"    > [bold]Description:[/] {self.__description}")

        return profile_info

    @override
    def __str__(self) -> str:
        return f"{self.__name.title()}'s profile"
