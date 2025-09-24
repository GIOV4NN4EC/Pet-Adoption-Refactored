import questionary

from datetime import date


def create_date() -> date | bool:
    day: str = questionary.text("Type the day:",
                                validate=lambda text: True if int(text) >= 1 and
                                int(text) <= 31 else "Invalid day",
                                qmark=">>").ask()
    if date is None:
        return False

    month: str = questionary.text("Type the month:",
                                  validate=lambda text: True if int(text) >= 1 and
                                  int(text) <= 12 else "Invalid month",
                                  qmark=">>").ask()
    if month is None:
        return False

    year: str = questionary.text("Type the year:",
                                 validate=lambda text: True if int(text) >= 1
                                 else "Invalid year",
                                 qmark=">>").ask()

    if year is None:
        return False

    return date(int(year), int(month), int(day))
