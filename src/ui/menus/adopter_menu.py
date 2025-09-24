from datetime import date
from typing import Any
import questionary
from rich.console import Console
from rich.panel import Panel

from src.adopter import Adopter

from src.application import Application
from src.donation import Donation
from src.form import Form
from src.query.query import Query
from src.shelter import Shelter
from src.pet import Pet

from src.ui.lister import Lister
from src.ui.name_validator import NameValidator

from src.ui.menus.menu import Menu
from src.ui.menus.social_menu import SocialMenu
from src.ui.menus.listing_menu import ListingMenu


class AdopterMenu(Menu):
    def __init__(self, user: Adopter, console: Console):
        Menu.__init__(self, user, console)
        self.name = "adopter menu"

        self.actions.update({
            "Search Pets": {
                "func": self.search_pet,
                "args": []},

            "Filter Pets": {
                "func": self.filter_pets,
                "args": []},

            "Apply to Adopt a Pet": {
                "func": self.apply_adopt,
                "args": []},

            "View Adoption Applications": {
                "func": self.show_applications,
                "args": []},

            "Donate to a Shelter": {
                "func": self.donate,
                "args": []}
        })

        self.add_submenu("Social Feed", SocialMenu(user, console), [])
        self.add_submenu("System Items", ListingMenu(user, console), [])

    def donate(self):
        self.console.print()
        shelters = [f"{shelter}" for shelter in Shelter.data.values()]

        self.console.print()
        name: str = questionary.select("Which shelter do you want to donate to?",
                                       choices=shelters).ask()
        name = name.split(" - ")[0][1:]

        ammount: str = questionary.text("How much to you want to donate?",
                                        validate=lambda text: True if float(text) > 0 else "Ammount must be positive").ask()

        d = Donation(self.user.username, name, float(ammount), date.today())

        self.console.print(f"\nDonation registered!\n >{d}")

        questionary.press_any_key_to_continue().ask()

    def get_pet_by_name(self):
        self.console.print()
        name: str = questionary.text("Type the pet's name:",
                                     validate=NameValidator,
                                     qmark=">>").ask()

        if Pet.__contains__(name):
            return Pet.data[name]

        self.console.print("\nPet not found\n")
        questionary.press_any_key_to_continue().ask()

        return None

    def make_form(self, form: Form) -> list[dict[str, str | list]]:
        questions_dict: list[dict[str, str | list]] = []
        for question in form:
            questions_dict.append({
                "type": "select",
                "name": question.name,
                "message": question.name,
                "choices": question.options
            })
        return questions_dict

    def apply_adopt(self):
        pet: Pet | None = self.get_pet_by_name()

        if pet is None:
            return

        if pet.is_adopted():
            self.console.print(f"{pet.profile.name}'s alreaty adopted")
            questionary.press_any_key_to_continue().ask()
            return

        if Application.__contains__(f"{pet.profile.name}-{self.user.username}"):
            self.console.print(
                f"{self.user.username} already applied to adopt {pet.profile.name}")
            questionary.press_any_key_to_continue().ask()
            return

        questions_dict: list[dict[str, str | list]] = self.make_form(pet.form)

        self.console.print(
            "\nAnswer the following questions to fill an adoption application!\n")
        answers_dict: dict[str, str] = questionary.prompt(questions_dict)
        answers_list: list[str] = list(answers_dict.values())

        ap = Application(self.user.username, pet.profile.name,
                         pet.form, answers_list)

        self.console.print("\nApplication submitted!")
        self.console.print(f"  > {ap}\n")

        questionary.press_any_key_to_continue().ask()

    def show_applications(self):
        apps: list[Application] = Application.get_apps_applicant(
            self.user.username)

        self.console.print()
        Lister(f"{self.user.name}'s Adoption Applications",
               apps, self.console).detailed_list()

    def filter_pets(self):
        pets: list[dict[str, Any]] = [pet.dictionary()
                                      for pet in Pet.data.values()]

        self.console.print(
            "\nTo filter pets, mark the desired characteristics.\n")

        filtered_names: list[str] = Query(pets).filter_items()

        if len(filtered_names) == 0:
            self.console.print("Your query had no results.")
            questionary.press_any_key_to_continue().ask()
            return

        fitlered_pets: list[Pet] = [Pet.data[name] for name in filtered_names]

        self.console.print(
            f"\nYour query provided {len(filtered_names)} results:\n")

        Lister("Filtered Pets", fitlered_pets, self.console).detailed_list()
        return

    def search_pet(self) -> None:
        pet: Pet | None = self.get_pet_by_name()

        if pet is None:
            return None

        self.console.print()
        pet_string: str = "\n".join(pet.formatted_list())
        self.console.print(Panel.fit(pet_string, title="Found Pet"))

        self.console.print()
        questionary.press_any_key_to_continue().ask()
