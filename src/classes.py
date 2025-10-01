from __future__ import annotations

from datetime import date
from abc import ABC, abstractmethod
from typing_extensions import Self
from typing_extensions import override
from dateutil import relativedelta
from typing import Any, TYPE_CHECKING
from copy import deepcopy

from src.prototype import Prototype


class Model(ABC):
    def __init_subclass__(cls):
        cls.data: dict[str, Self] = {}
        return super().__init_subclass__()

    @classmethod
    def __contains__(cls, item: str) -> bool:
        return item in cls.data.keys()

    @abstractmethod
    def formatted_list(self) -> list[str]:
        """returns all info in a formated list"""
        pass




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
    

#FACTORY MODE FOR USER
class UserFactory:
    @staticmethod
    def create_user(user_type: str, username: str, name: str) -> User:
        if user_type == "Adopter":
            return Adopter(username, name)
        elif user_type == "Shelter":
            return Shelter(username, name)
        else:
            raise ValueError(f"Unknown user type: {user_type}")

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




class Address:
    def __init__(self, street: str, district: str, number: str,
                 postal_code: int, city: str, state: str):
        self.__street: str = street
        self.__district: str = district
        self.__number: str = number
        self.__postal_code: int = postal_code
        self.__city: str = city
        self.__state: str = state

    @property
    def city(self) -> str:
        return self.__city

    @property
    def state(self) -> str:
        return self.__state

    @override
    def __str__(self) -> str:
        return (f"{self.__street}, {self.__number}, {self.__district} - "
                + f"{self.__city}/{self.__state}")



class Adopter(User):
    def __init__(self, username: str, name: str):
        User.__init__(self, username, name)
        self.allowed_post_types.append("success story")
        self.__pets: list[str] = []

    def formatted_list(self) -> list[str]:
        return self.profile.formatted_list()



class Answer:
    def __init__(self, question: Question, user_option: str):
        if user_option not in question:
            raise Exception(
                f"{user_option} is not a valid option for this question")

        self.__question: Question = question
        self.__user_option: str = user_option
        self.__is_preferred: bool = self.__user_option == self.__question.preferred_answer

    def __str__(self) -> str:
        if self.__is_preferred:
            marker = ":white_check_mark:"
            style = "green"
        else:
            marker = ":cross_mark:"
            style = "red"

        return f"> {self.__question.name}\n  R: [{style}]{self.__user_option} {marker}[/]"

    def __bool__(self) -> bool:
        return self.__is_preferred
    


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
    


class Donation(Model):
    @classmethod
    def by_donor(cls, donor: str) -> list['Donation']:
        return [don for don in cls.data.values() if don.__donor == donor]

    @classmethod
    def by_receiver(cls, receiver: str) -> list['Donation']:
        return [don for don in cls.data.values() if don.__receiver == receiver]

    @classmethod
    def by_user(cls, user: str) -> list['Donation']:
        return [don for don in cls.data.values() if don.__receiver == user or don.__donor == user]

    def __init__(self, donor: str, receiver: str, ammount: float,
                 donation_date: date):
        self.__donor: str = donor
        self.__receiver: str = receiver
        self.__ammount: float = ammount
        self.__donation_date: date = donation_date

        self.data[str(len(self.data))] = self

    @property
    def donor(self) -> str:
        return self.__donor

    @property
    def receiver(self) -> str:
        return self.__receiver

    @property
    def ammount(self) -> float:
        return self.__ammount

    @property
    def date(self) -> str:
        return self.__donation_date.isoformat()

    @override
    def __str__(self) -> str:
        return f"{Adopter.data[self.__donor].name} has donated [yellow]US${self.__ammount:.2f}[/] to {Shelter.data[self.__receiver].name}"

    @override
    def formatted_list(self) -> list[str]:
        return [self.__str__()]

    # overloading comparison operators
    def __gt__(self, other):
        if isinstance(other, Donation):
            return self.ammount > other.ammount
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Donation):
            return self.ammount < other.ammount
        return NotImplemented
    


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
    


class Form(Model, Prototype):
    def __init__(self, name: str, questions: list[Question] = []):
        self.name = name
        self.__questions: list[Question] = questions
        self.data[name] = self

    def add_question(self, name: str, options: list[str], right: str):
        if name in [q.name for q in self.__questions]:
            raise ValueError(f"question '{name}' already exists")

        self.__questions.append(Question(name, options, right))

    def clone(self) -> "Form":
        return deepcopy(self)

    def __len__(self) -> int:
        return len(self.__questions)

    def __getitem__(self, index: int) -> Question:
        return self.__questions[index]

    def __delitem__(self, index: int) -> None:
        del self.__questions[index]
        return None

    def __iter__(self):
        return iter(self.__questions)

    def __str__(self) -> str:
        return f"Adoption Application Form with {len(self)} questions"

    def formatted_list(self) -> list[str]:
        form: list[str] = ["Adoption Application Form", ""]

        for q in self.__questions:
            form.extend(q.formatted_list())
            form.append("")

        return form
    
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
    
    @form.setter
    def form(self, new_form: Form):
        self.__form = new_form


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



class PetProfileBuilder:
    def __init__(self, name: str):
        self._name = name
        self._birth = None
        self._address = None
        self._description = None
        self._breed = None
        self._color = None

    def with_birth(self, birth: date):
        self._birth = birth
        return self

    def with_address(self, address: Address):
        self._address = address
        return self

    def with_description(self, desc: str):
        self._description = desc
        return self

    def with_breed(self, breed: str):
        self._breed = breed
        return self

    def with_color(self, color: str):
        self._color = color
        return self

    def build(self) -> PetProfile:
        return PetProfile(
            self._name,
            birth=self._birth,
            address=self._address,
            description=self._description,
            breed=self._breed,
            color=self._color
        )


class Post(Model):
    def __init__(self, author: User, post_type: str,
                 title: str, content: str):
        if post_type not in author.allowed_post_types:
            raise Exception(f"{author.username} can't post {post_type}")

        self.__author: User = author
        self.__post_type: str = post_type
        self.__title: str = title
        self.__content: str = content

        self.__comments: list['Post'] = []
        self.__likes: list[str] = []

        self.data[title] = self

    @property
    def author(self) -> str:
        return self.__author.username

    @property
    def title(self) -> str:
        return self.__title

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, new_content: str) -> None:
        if len(new_content) == 0:
            raise ValueError("New content can't be empty")

        self.__content = new_content

    @property
    def comments(self) -> list['Post']:
        return self.__comments

    def add_comment(self, new_comment: 'Post') -> None:
        self.__comments.append(new_comment)

        return None

    @property
    def likes(self) -> int:
        """returns only the ammount of likes"""

        return len(self.__likes)

    def user_liked(self, u: str) -> bool:
        return u in self.__likes

    def like(self, liker: str) -> None:
        if self.user_liked(liker):
            raise ValueError("this user already liked this post")

        self.__likes.append(liker)
        return None

    def dislike(self, liker: str) -> None:
        if self.user_liked(liker):
            self.__likes.remove(liker)
            return None

        raise ValueError("this user did not liked this post")

    def formatted_title(self) -> str:
        title: str = f"{self.__post_type.title()} post by "
        title += f"{self.__author.name.title()} ({self.__author})"
        title += f"\nᯓ➤ {self.__title.upper()}\n"

        return title

    def formatted_footer(self) -> str:
        return f"\n:speech_balloon: {len(self.__comments)} commentss :heart: {self.likes} likes"

    def __str__(self) -> str:
        return f"{self.__post_type} by {self.__author}"

    def formatted_list(self) -> list[str]:
        """Generates a list of strings with the post's info formatted"""

        post_info: list[str] = []

        post_info.append(f"{self.__post_type.title()} post by "
                         + f"{self.__author.name.title()} ({self.__author})")

        post_info.append(f"\nᯓ➤ {self.__title.upper()}")
        post_info.append("")
        # post_info.extend(textwrap.wrap(self.__content,
        #                                initial_indent="  ╰┈➤ ",
        #                                subsequent_indent="      "))
        post_info.append(self.__content)
        post_info.append("")
        post_info.append(
            f"  :speech_balloon: {len(self.__comments)} commentss :heart: {self.likes} likes")

        return post_info



class Question(Prototype):
    def __init__(self, name: str, options: list[str], preferred_answer: str):
        if len(name) < 5:
            raise ValueError("question is too short")

        if name[-1] != "?":
            name = name + "?"

        self.__name: str = name
        self.__options: list[str] = options
        self.__preferred_answer: str = preferred_answer

    @property
    def name(self) -> str:
        return self.__name

    @property
    def options(self) -> list[str]:
        return self.__options

    @property
    def preferred_answer(self) -> str:
        return self.__preferred_answer

    def clone(self) -> "Question":
        return deepcopy(self)

    def formatted_list(self) -> list[str]:
        question_info: list[str] = [f"> {self.__name}"]
        question_info.extend([f"    - {option}" for option in self.__options])

        return question_info

    def __iter__(self):
        return iter(self.__options)

    def __len__(self):
        return len(self.__options)

    def __str__(self) -> str:
        return f"{self.name} [{len(self)} options]"



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





