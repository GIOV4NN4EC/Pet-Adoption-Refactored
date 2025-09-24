from .user import User


class Shelter(User):
    def __init__(self, username: str, name: str):
        User.__init__(self, username, name)
        self.__allowed_pet_types: list[str] = []
        self.allowed_post_types.append("educational")

    @property
    def allowed_pet_types(self) -> str:
        return ", ".join(self.__allowed_pet_types)

    def add_allowed_pet_type(self, pet_type: str) -> None:
        if len(pet_type) == 0:
            raise ValueError("pet type can't be empty")

        self.__allowed_pet_types.append(pet_type)
        return None

    def is_allowed(self, pet_type: str) -> bool:
        return pet_type in self.__allowed_pet_types

    def formatted_list(self) -> list[str]:
        shelter_info: list[str] = self.profile.formatted_list()
        shelter_info.append(
            f"    > [bold]Allowed pets[/]: {self.allowed_pet_types}")
        return shelter_info
