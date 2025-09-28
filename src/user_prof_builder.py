from datetime import date
from src.address import Address
from src.user_profile import Profile


class UserProfileBuilder:
    def __init__(self):
        self._name: str | None = None
        self._birth: date | None = None
        self._address: Address | None = None
        self._desc: str | None = None

    def set_name(self, name: str) -> "UserProfileBuilder":
        self._name = name
        return self

    def set_birth(self, birth: date | None) -> "UserProfileBuilder":
        self._birth = birth
        return self

    def set_address(self, address: Address | None) -> "UserProfileBuilder":
        self._address = address
        return self

    def set_desc(self, desc: str | None) -> "UserProfileBuilder":
        self._desc = desc
        return self

    def build(self) -> Profile:
        if not self._name:
            raise ValueError("O nome é obrigatório para criar um perfil de usuário")

        return Profile(
            name=self._name,
            birth=self._birth,
            address=self._address,
            description=self._desc
        )
