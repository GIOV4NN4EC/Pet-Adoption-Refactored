import questionary

from src.address import Address

from src.ui.name_validator import NameValidator


def create_address() -> Address | bool:

    street: str = questionary.text(
        "Address' street:", validate=NameValidator).ask()

    if street is None:
        return False

    district: str = questionary.text(
        "Address' district:", validate=NameValidator).ask()

    if district is None:
        return False

    number: str = questionary.text(
        "Address' number:", validate=NameValidator).ask()

    if number is None:
        return False

    postal_code: int = int(questionary.text(
        "Address' postal code:", validate=NameValidator).ask())

    if postal_code is None:
        return False

    city: str = questionary.text(
        "Address' city:", validate=NameValidator).ask()

    if city is None:
        return False

    state: str = questionary.text(
        "Address' state:", validate=NameValidator).ask()

    if state is None:
        return False

    return Address(street, district, number, postal_code, city, state)
