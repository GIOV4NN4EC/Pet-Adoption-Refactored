from datetime import date

import questionary

from rich.align import Align
from rich.console import Console
from rich.panel import Panel

from src.address import Address
from src.pet_profile import PetProfile
from src.user import User
from src.user_profile import Profile
from src.pet import Pet

from src.ui.name_validator import NameValidator


class ProfileUpdater():
    def __init__(self, profile_owner: User | Pet, console: Console):
        self.profile_owner: User | Pet = profile_owner
        self.profile: Profile = profile_owner.profile
        self.console: Console = console

    def update_updater(self, new_owner: User | Pet):
        self.profile_owner = new_owner
        self.profile = new_owner.profile

    def __update_name(self) -> bool:
        update: bool = questionary.confirm("Update name?").ask()
        if not update:
            return False

        self.console.print()

        new_name: str = questionary.text("New name:").ask()
        if new_name:
            self.profile.name = new_name
            return True
        return False

    def __update_birth(self) -> bool:
        update: bool = questionary.confirm("Update birth date?").ask()
        if not update:
            return False

        self.console.print()

        new_date: str = questionary.text("New birth day:",
                                         validate=lambda text: True if int(text) >= 1 and
                                         int(text) <= 31 else "Invalid date").ask()
        if new_date is None:
            return False

        new_month: str = questionary.text("New birth month:",
                                          validate=lambda text: True if int(text) >= 1 and
                                          int(text) <= 12 else "Invalid date").ask()
        if new_month is None:
            return False

        new_year: str = questionary.text("New birth year:",
                                         validate=lambda text: True if int(text) >= 1 and
                                         int(text) <= date.today().year else "Invalid date").ask()

        if new_year is None:
            return False

        new_birth: date = date(int(new_year), int(new_month), int(new_date))

        if new_birth <= date.today():
            self.profile.birth = new_birth
            return True
        return False

    def __update_address(self) -> bool:
        update: bool = questionary.confirm("Update address?").ask()
        if not update:
            return False

        self.console.print()

        new_street: str = questionary.text(
            "New street:", validate=NameValidator).ask()

        if new_street is None:
            return False

        new_district: str = questionary.text(
            "New district:", validate=NameValidator).ask()

        if new_district is None:
            return False

        new_number: str = questionary.text(
            "New number:", validate=NameValidator).ask()

        if new_number is None:
            return False

        new_postal_code: int = int(questionary.text(
            "New postal code:", validate=NameValidator).ask())

        if new_postal_code is None:
            return False

        new_city: str = questionary.text(
            "New city:", validate=NameValidator).ask()

        if new_city is None:
            return False

        new_state: str = questionary.text(
            "New state:", validate=NameValidator).ask()

        if new_state is None:
            return False

        new_address: Address = Address(
            new_street, new_district, new_number, new_postal_code, new_city, new_state)

        self.profile.address = new_address
        return True

    def __update_description(self):
        update: bool = questionary.confirm("Update description?").ask()
        if not update:
            return False

        self.console.print()

        new_description: str = questionary.text(
            "New description:", validate=NameValidator).ask()

        if new_description is None:
            return False

        self.profile.description = new_description
        return True

    def __update_breed(self):
        if not isinstance(self.profile, PetProfile):
            return

        update: bool = questionary.confirm("Update breed?").ask()
        if not update:
            return False

        self.console.print()

        new_breed: str = questionary.text(
            "New breed:", validate=NameValidator).ask()

        if new_breed is None:
            return False

        self.profile.breed = new_breed
        return True

    def __update_color(self):
        if not isinstance(self.profile, PetProfile):
            return

        update: bool = questionary.confirm("Update color?").ask()
        if not update:
            return False

        self.console.print()

        new_color: str = questionary.text(
            "New color:", validate=NameValidator).ask()

        if new_color is None:
            return False

        self.profile.color = new_color
        return True

    def update_profile(self):
        self.console.print(
            "\nLet's update this profile! Here's your current info!\n")

        self.console.print(Panel.fit("\n".join(self.profile_owner.formatted_list()),
                                     title="Current Profile"))

        update = [["name", self.__update_name, False],
                  ["birth", self.__update_birth, False],
                  ["address", self.__update_address, False],
                  ["description", self.__update_description, False]]

        if isinstance(self.profile_owner, Pet):
            update.extend([["breed", self.__update_breed, False],
                          ["color", self.__update_color, False]])

        for item in update:
            self.console.print()
            item[2] = item[1]()

        self.console.print("\nThe following items were updated:")
        for item in update:
            if item[2]:
                self.console.print(f"> {item[0]}")

        self.console.print("\nHere's the new profile!")

        self.console.print(Panel.fit("\n".join(self.profile_owner.formatted_list()),
                                     title="Current Profile"))
