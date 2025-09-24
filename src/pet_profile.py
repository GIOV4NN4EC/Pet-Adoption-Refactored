from datetime import date
from typing_extensions import override

from src.address import Address
from src.user_profile import Profile


class PetProfile(Profile):
    def __init__(self, name: str,
                 birth: date | None = None,
                 address: Address | None = None,
                 description: str | None = None,
                 breed: str | None = None,
                 color: str | None = None):
        super().__init__(name, birth, address, description)
        self.__breed: str | None = breed
        self.__color: str | None = color

    def dictionary(self) -> dict[str, int | str | None]:
        d = Profile.dictionary(self)
        d.update({
            "breed": self.__breed,
            "color": self.__color
        })
        return d

    @property
    def breed(self) -> str | None:
        """returns None if no breed was added to profile"""

        return self.__breed

    @breed.setter
    def breed(self, new_breed: str):
        if len(new_breed) > 0:
            self.__breed = new_breed

    @property
    def color(self) -> str | None:
        """returns None if no breed was added to profile"""

        return self.__color

    @color.setter
    def color(self, new_color: str):
        if len(new_color) > 0:
            self.__color = new_color

    @override
    def as_list(self) -> list[str]:
        info: list[str] = Profile.as_list(self)

        if self.__breed:
            info.append(self.__breed)

        if self.__color:
            info.append(self.__color)

        return info

    @override
    def formatted_list(self) -> list[str]:
        profile_info: list[str] = Profile.formatted_list(self)

        if self.breed:
            profile_info.append(f"    > [bold]Breed:[/] {self.breed}")

        if self.color:
            profile_info.append(f"    > [bold]Color:[/] {self.color}")

        return profile_info
