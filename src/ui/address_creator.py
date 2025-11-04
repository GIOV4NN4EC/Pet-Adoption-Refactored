from src.exceptions import EmptyFieldError, InvalidPostalCodeError, InvalidAddressError
from src.classes import Address
import questionary

def create_address() -> Address | bool:
    try:
        street = questionary.text("Street:").ask()

        if not street:
            raise EmptyFieldError("Street cannot be empty.")

        district = questionary.text("District:").ask()

        if not district:
            raise EmptyFieldError("District cannot be empty.")

        number = questionary.text("Number:").ask()

        if not number:
            raise EmptyFieldError("Number cannot be empty.")

        postal_code = questionary.text("Postal code:").ask()
        
        if not postal_code.isdigit():
            raise InvalidPostalCodeError("Postal code must be numeric.")

        city = questionary.text("City:").ask()
        state = questionary.text("State:").ask()

        if not city or not state:
            raise InvalidAddressError("City and state cannot be empty.")

        return Address(street, district, number, int(postal_code), city, state)

    except (EmptyFieldError, InvalidPostalCodeError, InvalidAddressError) as e:
        print(f"[Address Error] {e}")
        return False
