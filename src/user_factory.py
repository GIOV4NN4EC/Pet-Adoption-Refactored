import questionary
from rich.console import Console

from src.adopter import Adopter
from src.shelter import Shelter
from src.user_prof_builder import UserProfileBuilder


console = Console()


class UserFactory:
    @staticmethod
    def sign_up(user_type: str) -> Adopter | Shelter:
        while True:
            console.print()
            username: str = questionary.text("Choose an username: ").ask()

            if user_type == "Adopter":
                if Adopter.username_available(username):
                    first_name: str = questionary.text("What's your first name?").ask()
                    last_name: str = questionary.text("What's your last name?").ask()
                    full_name: str = f"{first_name.title()} {last_name.title()}"

                    # usando o builder para criar o profile
                    profile = (
                        UserProfileBuilder()
                        .set_name(full_name)
                        .set_desc("Adopter profile")
                        .build()
                    )

                    return Adopter(username, profile)

            elif user_type == "Shelter":
                if Shelter.username_available(username):
                    name: str = questionary.text("What's the shelter's name?").ask()

                    # usando o builder para criar o profile
                    profile = (
                        UserProfileBuilder()
                        .set_name(name.title())
                        .set_desc("Shelter profile")
                        .build()
                    )

                    return Shelter(username, profile)

            console.print("Username taken.\n", style="red")