from src.adopter import Adopter
from src.answer import Answer
from src.form import Form
from src.model import Model
from src.pet import Pet


class Application(Model):
    @classmethod
    def get_apps_pet(cls, pet: str) -> list['Application']:
        return [app for app in cls.data.values() if app.__pet == pet]

    @classmethod
    def get_apps_applicant(cls, applicant: str) -> list['Application']:
        return [app for app in cls.data.values() if app.__applicant == applicant]

    def __init__(self, applicant: str, pet: str,
                 pet_form: Form, answers: list[str]):
        if len(answers) != len(pet_form):
            raise Exception(
                f"{len(answers)} answers for {len(pet_form)} questions")

        if applicant in [apps.__applicant for apps in Application.get_apps_pet(pet)]:
            raise Exception(f"{applicant} already applied to adopt {pet}")

        self.__applicant: str = applicant
        self.__pet: str = pet

        self.__answers: list[Answer] = []
        self.__status: str = "in review"
        self.feedback: str

        right_answers: int = 0
        for index, question in enumerate(pet_form):
            answer = Answer(question, answers[index])
            self.__answers.append(answer)
            right_answers += 1 if answer else 0

        self.__score: float = right_answers / len(pet_form)

        self.data[f"{pet}-{applicant}"] = self
        Pet.data[pet].add_application()

    @property
    def applicant(self) -> str:
        return self.__applicant

    @property
    def pet(self) -> str:
        return self.__pet

    @property
    def score(self) -> float:
        return self.__score

    def approve(self) -> None:
        self.__status = "approved"
        Pet.data[self.__pet].tutor = Adopter.data[self.__applicant]
        Pet.data[self.__pet].was_adopted()
        return None

    def deny(self, feedback: str) -> None:
        self.__status = "denied"
        self.feedback = feedback
        return None

    def __str__(self) -> str:
        return f"[bold on purple4]@{self.__applicant}'s application to adopt {self.__pet.title()}[/]"

    # OVERRIDE FOR POLYMORPHISM

    def formatted_list(self) -> list[str]:
        application_info: list[str] = [f"{self}", ""]

        for answer in self.__answers:
            application_info.append(f"{answer}")
            application_info.append("")

        application_info.append(
            f"Score: [repr.number]{self.__score * 100:.2f}%[/]")

        application_info.append(
            f"Status: {self.__status.upper()}"
        )

        return application_info
