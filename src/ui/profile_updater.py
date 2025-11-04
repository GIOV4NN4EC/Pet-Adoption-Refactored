from datetime import date

import questionary

from rich.align import Align
from rich.console import Console
from rich.panel import Panel

from src.classes import Address, PetProfile, User, Profile, Pet
from src.exceptions import InvalidDateError, InvalidPostalCodeError, InvalidAddressError

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

        try:
            new_date: str = questionary.text("New birth day:").ask()
            new_month: str = questionary.text("New birth month:").ask()
            new_year: str = questionary.text("New birth year:").ask()

            if not (new_date.isdigit() and new_month.isdigit() and new_year.isdigit()):
                raise InvalidDateError("All date fields must be numeric.")

            day, month, year = int(new_date), int(new_month), int(new_year)

            if not (1 <= day <= 31) or not (1 <= month <= 12):
                raise InvalidDateError("Invalid day or month entered.")

            if year > date.today().year:
                raise InvalidDateError("Birth year cannot be in the future.")

            new_birth: date = date(year, month, day)

            if new_birth > date.today():
                raise InvalidDateError("Birth date cannot be in the future.")

            self.profile.birth = new_birth
            return True

        except InvalidDateError as e:
            self.console.print(f"[Invalid date] {e}")
            return False
        except ValueError:
            self.console.print("[Invalid date] Please enter valid numeric values.")
            return False


    def __update_address(self) -> bool:
        update: bool = questionary.confirm("Update address?").ask()
        if not update:
            return False

        self.console.print()

        try:
            new_street = questionary.text("New street:", validate=NameValidator).ask()
            new_district = questionary.text("New district:", validate=NameValidator).ask()
            new_number = questionary.text("New number:", validate=NameValidator).ask()
            new_postal_code = questionary.text("New postal code:", qmark=">>").ask()
            new_city = questionary.text("New city:", validate=NameValidator).ask()
            new_state = questionary.text("New state:", validate=NameValidator).ask()

            # VERIFYING EMPTY FIELDS
            if not all([new_street, new_district, new_number, new_postal_code, new_city, new_state]):
                raise InvalidAddressError("All address fields must be filled.")


            if not new_postal_code.isdigit():
                raise InvalidPostalCodeError("Postal code must contain only digits.")

            postal_code_int = int(new_postal_code)
            if postal_code_int <= 0:
                raise InvalidPostalCodeError("Postal code must be a positive number.")

            new_address = Address(
                new_street, new_district, new_number, postal_code_int, new_city, new_state
            )
            self.profile.address = new_address
            return True

        except (InvalidAddressError, InvalidPostalCodeError) as e:
            self.console.print(f"[Address error] {e}")
            return False


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
