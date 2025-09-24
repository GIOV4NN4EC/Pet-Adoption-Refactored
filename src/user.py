from abc import ABC
from typing_extensions import Self, override

from src.model import Model
from src.user_profile import Profile


class User(Model, ABC):
    @classmethod
    def username_available(cls, username: str) -> bool:
        if username in cls.data.keys():
            return False

        return True

    @classmethod
    def login(cls, username: str) -> Self:
        return cls.data[username]

    def __init__(self, username: str, name: str):
        self.__username: str = username
        self.profile: Profile = Profile(name)
        self.allowed_post_types: list[str] = ["forum", "comment"]
        self.data[username] = self

    @property
    def username(self) -> str:
        return self.__username

    @property
    def name(self) -> str:
        return self.profile.name

    @override
    def __str__(self) -> str:
        return f"@{self.__username} - {self.profile.name}"
