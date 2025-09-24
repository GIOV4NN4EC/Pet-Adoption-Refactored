from typing import Iterable

import questionary
from rich.console import Console
from rich.panel import Panel


class Lister:
    def __init__(self, items_name: str, items: Iterable, console: Console):
        self.items_name = items_name
        self.items = items
        self.console = console

    def update(self, new_name, new_items):
        self.items_name = new_name
        self.items = new_items

    def simple_list(self):
        formatted = ""
        for item in self.items:
            formatted += f"\n> {item}"

        self.console.print(
            Panel.fit(formatted, title=f"{self.items_name.upper()}"))

        questionary.press_any_key_to_continue().ask()

    # POLYMORPHISM

    def detailed_list(self):
        formatted = ""
        for item in self.items:
            formatted += "\n" + "\n".join(item.formatted_list()) + "\n"

        self.console.print(
            Panel.fit(formatted, title=f"{self.items_name.upper()}"))

        questionary.press_any_key_to_continue().ask()
