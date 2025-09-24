import questionary

from rich.console import Console

from src.user import User

from src.ui.profile_updater import ProfileUpdater
from src.ui.header import header
from src.ui.clean import clear_screen


class Menu:
    def __init__(self, user: User, console: Console):

        self.name = "main menu"
        self.loop: bool = True
        self.user: User = user
        self.console: Console = console
        self.profile_updater: ProfileUpdater = ProfileUpdater(user, console)

        self.actions = {
            "Return to Welcome Page":
                {"func": self.go_back,
                 "args": []},

            "Update Profile":
                {"func": self.profile_updater.update_profile,
                 "args": []}
        }

    def add_submenu(self, name: str, menu: 'Menu', args):
        self.actions[name] = {
            "func": menu.show_menu,
            "args": args
        }

    def wip(self):
        self.console.print("\nWe're still working on this one...\n")
        questionary.press_any_key_to_continue().ask()

    def go_back(self):
        self.loop = False

    def show_menu(self):
        self.loop = True
        while self.loop:

            clear_screen()
            self.console.print(header(self.name))
            self.console.print()
            option = questionary.select("Choose an option:",
                                        choices=list(self.actions.keys())).ask()

            self.actions[option]["func"](*self.actions[option]["args"])
