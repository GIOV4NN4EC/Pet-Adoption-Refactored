# EXCEPTIONS ABOUT DATA ENTRY

class InvalidDateError(Exception):
    """Raised when an invalid date is entered."""
    pass

class InvalidAddressError(Exception):
    """Raised when the address provided is incomplete or invalid."""
    pass

class InvalidNameError(Exception):
    """Raised when the provided name is invalid."""
    pass

class EmptyFieldError(Exception):
    """Raised when a required field is left empty."""
    pass

class InvalidPostalCodeError(Exception):
    """Raised when the provided postal code is not numeric or invalid."""
    pass


class MissingAddressFieldError(Exception):
    """Raised when one or more required address fields are missing."""
    pass


class InvalidDonationAmountError(Exception):
    """Raised when the donation amount is zero or negative."""
    pass


# EXCEPTIONS PETMENU

class PetNotFoundError(Exception):
    """Raised when a pet does not exist in the system."""
    pass


class AdopterNotFoundError(Exception):
    """Raised when an adopter is not found."""
    pass


class ApplicationAlreadyExistsError(Exception):
    """Raised when an adopter already applied for the same pet."""
    pass


class InvalidAnswerError(Exception):
    """Raised when an invalid answer is provided for a question."""
    pass


class InvalidFormError(Exception):
    """Raised when a form has inconsistencies or missing answers."""
    pass


class OperationNotAllowedError(Exception):
    """Raised when a state transition or action is not allowed."""
    pass

class DuplicatePetNameError(Exception):
    """Raised when a shelter tries to register a pet with a name that already exists."""
    pass
