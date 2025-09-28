from datetime import date
from src.address import Address
from src.pet_profile import PetProfile


class PetProfileBuilder:

    def __init__(self):
        self._name: str = ""
        self._birth: date | None = None
        self._address: Address | None = None
        self._description: str | None = None
        self._breed: str | None = None
        self._color: str | None = None

    def set_name(self, name: str) -> "PetProfileBuilder":
        self._name = name
        return self

    def set_birth(self, birth: date) -> "PetProfileBuilder":
        self._birth = birth
        return self

    def set_address(self, address: Address) -> "PetProfileBuilder":
        self._address = address
        return self

    def set_description(self, description: str) -> "PetProfileBuilder":
        self._description = description
        return self

    def set_breed(self, breed: str) -> "PetProfileBuilder":
        self._breed = breed
        return self

    def set_color(self, color: str) -> "PetProfileBuilder":
        self._color = color
        return self

    def build(self) -> PetProfile:
        if not self._name:
            raise ValueError("The Pet needs a name!")

        return PetProfile(
            name=self._name,
            birth=self._birth,
            address=self._address,
            description=self._description,
            breed=self._breed,
            color=self._color
        )
