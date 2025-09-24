import questionary
from rich.console import Console

from src.event import Event
from src.user import User

from src.ui.address_creator import create_address
from src.ui.date_creator import create_date
from src.ui.name_validator import NameValidator
from src.ui.lister import Lister

from src.ui.menus.menu import Menu


class EventMenu(Menu):
    def __init__(self, user: User, console: Console):
        Menu.__init__(self, user, console)
        self.name = "event management"

        self.actions = {
            "Return to Main Menu": {
                "func": self.go_back,
                "args": []},

            "View Shelter's Events": {
                "func": self.show_events,
                "args": []},

            "Create Event": {
                "func": self.create_event,
                "args": []},

            "Cancel Event": {
                "func": self.cancel_event,
                "args": []},

            "Complete Event": {
                "func": self.complete_event,
                "args": []}
        }

    def create_event(self):
        self.console.print()
        name: str = questionary.text("Type the event's name:",
                                     validate=NameValidator,
                                     qmark=">>").ask()

        self.console.print()
        address = create_address()
        if address is False:
            return

        self.console.print()
        event_date = create_date()
        if event_date is False:
            return

        event = Event(name, event_date, address, self.user.username)

        self.console.print("\nEvent created!")
        self.console.print(f"  > {event}\n")

        questionary.press_any_key_to_continue().ask()

    def get_event_name(self) -> Event | None:
        self.console.print()
        name: str = questionary.text("Type the event's name:",
                                     validate=NameValidator,
                                     qmark=">>").ask()

        if Event.__contains__(name):
            return Event.data[name]

        self.console.print("\nEvent not found.")
        questionary.press_any_key_to_continue().ask()
        return None

    def cancel_event(self):
        event = self.get_event_name()

        if event is None:
            return

        event.cancel()
        self.console.log(f"\n{event.name} cancelled.\n")

        questionary.press_any_key_to_continue().ask()

    def complete_event(self):
        event = self.get_event_name()

        if event is None:
            return

        event.complete()
        self.console.log(f"\n{event.name} completed.\n")

        questionary.press_any_key_to_continue().ask()

    def show_events(self):
        events = Event.by_shelter(self.user.username)
        Lister(f"{self.user.name}'s events",
               events, self.console).detailed_list()
