from questionary import Validator, ValidationError
from src.exceptions import InvalidNameError, EmptyFieldError


class NameValidator(Validator):
    def validate(self, document):
        text = document.text.strip()

        # EmptyFieldError
        if not text:
            raise ValidationError(
                message=str(EmptyFieldError("Please enter a value")),
                cursor_position=len(document.text),
            )

        # InvalidNameError
        if not all(char.isalpha() or char.isspace() for char in text):
            raise ValidationError(
                message=str(InvalidNameError("Name can only contain letters")),
                cursor_position=len(document.text),
            )
