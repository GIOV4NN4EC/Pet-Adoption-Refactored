import questionary
from rich.console import Console

import initial_info

from src.adopter import Adopter
from src.shelter import Shelter

from src.ui.clean import clear_screen
from src.ui.header import header

from src.ui.menus.adopter_menu import AdopterMenu
from src.ui.menus.shelter_menu import ShelterMenu

# globals
console = Console()


def welcome() -> Adopter | Shelter | None:
    while True:
        clear_screen()

        console.print(header("Pet Adoption App"))
        console.print()

        user_type: str = questionary.select("Choose your role!",
                                            choices=["Quit", "Adopter", "Shelter"]).ask()

        if not user_type or user_type == "Quit":
            console.print("\nGoodbye!")
            return None

        console.print()

        user_access: str = questionary.select("How do you want to access PetApp?",
                                              choices=["Login", "Sign Up"]).ask()

        if user_access == "Login":
            user = login(user_type)
        elif user_access == "Sign Up":
            user = sign_up(user_type)
        else:
            continue

        if user:
            return user


def sign_up(user_type: str) -> Adopter | Shelter:
    while True:
        console.print()
        username: str = questionary.text("Choose an username: ").ask()

        if user_type == "Adopter":
            if Adopter.username_available(username):
                first_name: str = questionary.text(
                    "What's your first name?").ask()
                last_name: str = questionary.text(
                    "What's your last name?").ask()
                name: str = first_name.title() + " " + last_name.title()
                return Adopter(username, name)

        elif user_type == "Shelter":
            if Shelter.username_available(username):
                name: str = questionary.text(
                    "What's the shelter's name?").ask()
                return Shelter(username, name)

        console.print("Username taken.\n", style="red")


def login(user_type: str) -> Adopter | Shelter | None:
    console.print()
    username: str = questionary.text("Type your username: ").ask()

    if user_type == "Adopter":
        if not Adopter.username_available(username):
            return Adopter.login(username)
    elif user_type == "Shelter":
        if not Shelter.username_available(username):
            return Shelter.login(username)

    console.print("User not found.\n")
    questionary.press_any_key_to_continue().ask()
    return None


def main():
    user = welcome()
    if not user:
        return

    if isinstance(user, Adopter):
        adopter_menu: AdopterMenu = AdopterMenu(user, console)
        adopter_menu.show_menu()

    elif isinstance(user, Shelter):
        shelter_menu: ShelterMenu = ShelterMenu(user, console)
        shelter_menu.show_menu()

    main()


if __name__ == "__main__":
    initial_info.create_data()

    main()
