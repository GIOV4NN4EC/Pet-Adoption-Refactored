from .user import User


class Adopter(User):
    def __init__(self, username: str, name: str):
        User.__init__(self, username, name)
        self.allowed_post_types.append("success story")
        self.__pets: list[str] = []

    def formatted_list(self) -> list[str]:
        return self.profile.formatted_list()
