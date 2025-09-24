from rich.console import Console

from src.event import Event
from src.user import User
from src.shelter import Shelter
from src.donation import Donation

from src.ui.menus.menu import Menu
from src.ui.lister import Lister
from src.pet import Pet


class ListingMenu(Menu):
    def __init__(self, user: User, console: Console):
        Menu.__init__(self, user, console)

        self.name = "listing menu"

        self.actions = {
            "Return to Main Menu":
                {"func": self.go_back,
                 "args": []},

            "Show Shelters":
                {"func": self.show_shelters,
                 "args": []},

            "Show Pets":
                {"func": self.show_pets,
                 "args": []},

            "Show Events":
                {"func": self.show_events,
                 "args": []},

            "Show My Donations":
                {"func": self.show_my_donations,
                 "args": []},
        }

    def show_shelters(self):
        Lister("shelters", Shelter.data.values(), self.console).detailed_list()

    def show_pets(self):
        Lister("pets", Pet.data.values(), self.console).detailed_list()

    def show_events(self):
        Lister("events", Event.data.values(), self.console).detailed_list()

    def show_my_donations(self):
        Lister(f"{self.user.name}'s donations",
               Donation.by_user(self.user.username),
               self.console).simple_list()
