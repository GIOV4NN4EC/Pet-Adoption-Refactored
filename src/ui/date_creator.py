from src.exceptions import InvalidDateError
from datetime import date
import questionary

def create_date() -> date | bool:
    try:
        day = questionary.text("Type the day:").ask()
        
        if not day.isdigit() or not (1 <= int(day) <= 31):
            raise InvalidDateError("Invalid day entered.")

        month = questionary.text("Type the month:").ask()
        
        if not month.isdigit() or not (1 <= int(month) <= 12):
            raise InvalidDateError("Invalid month entered.")

        year = questionary.text("Type the year:").ask()
        
        if not year.isdigit() or int(year) < 1:
            raise InvalidDateError("Invalid year entered.")

        return date(int(year), int(month), int(day))

    except InvalidDateError as e:
        print(f"[Invalid date] {e}")
        return False
