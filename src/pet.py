from typing import Any
from dateutil import relativedelta
from datetime import date
from typing_extensions import override

# from src.application import Application
from src.form import Form
from src.model import Model
from src.pet_profile import PetProfile
from src.question import Question
from src.address import Address
from src.adopter import Adopter


class Pet(Model):
    @classmethod
    def by_shelter(cls, shelter: str) -> list['Pet']:
        return [pet for pet in cls.data.values() if pet.__shelter == shelter]

    def __init__(self, name: str, shelter: str, pet_type: str,
                 birth: date | None = None,
                 address: Address | None = None,
                 desc: str | None = None,
                 breed: str | None = None,
                 color: str | None = None):

        self.__shelter: str = shelter
        self.__pet_type: str = pet_type
        self.profile: PetProfile = PetProfile(name, birth, address,
                                              desc, breed, color)
        self.__status: str = "rescued"
        self.__form: Form = Form("standard",
                                 [Question(
                                     f"Are you sure you want to adopt {name}?",
                                     ["Yes", "No"],
                                     "Yes")])
        self.__applications: int = 0
        self.tutor: Adopter | None = None

        self.data[name] = self

    def dictionary(self) -> dict[str, Any]:
        pet_info: dict[str, Any] = {
            "pet_type": self.__pet_type,
            "shelter": self.__shelter,
            "status": self.__status
        }

        pet_info.update(self.profile.dictionary())

        return pet_info

    @property
    def form(self) -> Form:
        return self.__form

    def add_application(self) -> None:
        self.__applications += 1
        return None

    def is_adopted(self) -> bool:
        return self.__status == "adopted"

    def was_adopted(self) -> None:
        self.__status = "adopted"

    def add_template_question(self, question: str,
                              options: list[str],
                              answer: str) -> None:

        self.__form.add_question(question, options, answer)
        return None

    # OVERRIDE FOR POLYMORPHISM

    @override
    def formatted_list(self) -> list[str]:
        pet_info: list[str] = self.profile.formatted_list()

        pet_info.append(f"    > [bold]Pet type:[/] {self.__pet_type}")
        pet_info.append(f"    > [bold]Status:[/] {self.__status.upper()}")
        pet_info.append(
            f"    > [bold]Applications:[/] {self.__applications}")

        return pet_info

    def __str__(self) -> str:
        return f"{self.profile.name}: {self.__pet_type.title()}, {self.__status.upper()}, {self.__applications} applications"
