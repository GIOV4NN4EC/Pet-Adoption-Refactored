# external libraries
import questionary
from rich.console import Console
from rich.panel import Panel

# models
from src.application import Application
from src.user import User
from src.pet import Pet

# UI helpers
from src.ui.profile_updater import ProfileUpdater
from src.ui.name_validator import NameValidator
from src.ui.lister import Lister
from src.ui.clean import clear_screen
from src.ui.header import header

# menus
from src.ui.menus.menu import Menu


class PetMenu(Menu):
    def __init__(self, user: User, console: Console):
        Menu.__init__(self, user, console)
        self.name = "pet menu"

        self.updater: ProfileUpdater = ProfileUpdater(user, console)

        self.actions = {
            "Return to Main Menu": {
                "func": self.go_back,
                "args": []},

            "View Shelter's Pets": {
                "func": self.show_pets,
                "args": []},

            "Register New Pet": {
                "func": self.create_pet,
                "args": []},

            "Update Pet Profile": {
                "func": self.update_pet_profile,
                "args": []},

            "Add Question to Pet's Form": {
                "func": self.add_question,
                "args": []},

            "View Pet's Adoption Applications": {
                "func": self.view_applications,
                "args": []}

        }

    def show_pets(self):
        pets = Pet.by_shelter(self.user.username)
        Lister(f"{self.user.name}'s pets",
               pets,
               self.console).detailed_list()

    def get_pet_name(self) -> Pet | None:
        self.console.print()
        name: str = questionary.text("Type the pet's name:",
                                     validate=NameValidator,
                                     qmark=">>").ask()

        if Pet.__contains__(name):
            return Pet.data[name]

        return None

    def update_pet_profile(self):
        pet: Pet | None = self.get_pet_name()

        if pet is None:
            return

        self.updater.update_updater(pet)
        self.updater.update_profile()

    def create_pet(self):
        name: str = questionary.text("Type the pet's name:",
                                     validate=NameValidator,
                                     qmark=">>").ask()

        pet_type: str = questionary.text("Type the pet's type (species):",
                                         validate=NameValidator,
                                         qmark=">>").ask()

        if not self.user.is_allowed(pet_type):
            self.console.print(
                f"{self.user.name} does not shelters {pet_type}")
            return

        new_pet: Pet = Pet(name, self.user.username, pet_type,
                           address=self.user.profile.address)

        update: bool = questionary.confirm(
            f"Do you want to update {name}'s profile?").ask()

        if update:
            self.updater.update_updater(new_pet)
            self.updater.update_profile()

    def add_question(self):
        pet: Pet | None = self.get_pet_name()

        if pet is None:
            return

        self.console.print()

        name: str = questionary.text("Type your question:",
                                     validate=NameValidator,
                                     qmark=">>").ask()

        self.console.print()

        options: list[str] = []
        while True:
            option: str = questionary.text("Type a possible answer (or <q> to stop):",
                                           validate=NameValidator,
                                           qmark="·").ask()

            if option == "q" or option is None:
                break

            options.append(option)

        self.console.print()

        correct: str = questionary.text("Type the right answer:",
                                        validate=lambda text: True if text in options else "Right answer must be one of the provided options",
                                        qmark="✓", instruction="Choose one of the provided options as the correct answer for this question").ask()

        pet.add_template_question(name, options, correct)

    def deny_app(self, app: Application) -> int:
        self.console.print(f"\nDenying [bold]{app.applicant}'s[/] application to adopt [bold]{app.pet}[/]...",
                           f"\nPlease provide some feedback to {app.applicant}\n")
        feedback: str = questionary.text("Why was this application denied?",
                                         validate=NameValidator).ask()

        app.deny(feedback)
        return 0

    def approve_app(self, apps: list[Application], approved_app: Application) -> int:
        approved_app.approve()
        self.console.print(
            f"{approved_app.applicant}'s application to adopt {approved_app.pet} APPROVED! :party_popper:\n")

        questionary.press_any_key_to_continue().ask()

        self.console.print(
            "\nThis means all other applications must be denied. Let's give the other applicants some feedback!/n")

        questionary.press_any_key_to_continue(
            "Press any key to start...").ask()

        for app in apps:
            if app != approved_app:
                self.deny_app(app)

        return 0

    def next(self) -> int:
        return 1

    def previous(self, index: int) -> int:
        return -1 if index > 0 else 0

    def application_actions(self, index: int, current_app: Application,
                            apps: list[Application]) -> int:
        actions = {
            "Previous Application": {
                "func": self.previous,
                "args": [index]},

            "Approve Application": {
                "func": self.approve_app,
                "args": [apps, current_app]},

            "Deny Application": {
                "func": self.deny_app,
                "args": [current_app]},

            "Next Application": {
                "func": self.next,
                "args": []}

        }

        option = questionary.select("Choose an option",
                                    choices=list(actions.keys()),
                                    qmark=">>").ask()

        move: int = actions[option]["func"](*actions[option]["args"])

        return index + move

    def view_applications(self):
        pet: Pet | None = self.get_pet_name()

        if pet is None:
            return

        self.console.print()
        apps: list[Application] = Application.get_apps_pet(pet.profile.name)

        if len(apps) == 0:
            return

        index: int = 0
        while index < len(apps):
            clear_screen()
            self.console.print(header("APPLICATIONS"))

            self.console.print(
                Panel.fit("\n".join(apps[index].formatted_list())))
            self.console.print()

            index = self.application_actions(index, apps[index], apps)

        questionary.press_any_key_to_continue(
            "There are no more applications. Press any key to go back").ask()
