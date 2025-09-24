from typing import Any
import questionary


class Query:
    def __init__(self, items: list[dict[str, Any]]):
        self.items: list[dict[str, Any]] = items

    def get_options(self) -> dict[str, list[str]]:
        """Gets all options (as strings)"""

        options: dict[str, list[str]] = {}

        for dictionary in self.items:
            for key, value in dictionary.items():
                if value is not None and key != "name":
                    value_str = str(value)  # pra garantir a string
                    if key not in options:
                        options[key] = []
                    if value_str not in options[key]:
                        options[key].append(value_str)

        return options

    def make_form(self) -> list[dict[str, str | list]]:
        options = self.get_options()
        criteria_dicts: list[dict[str, str | list]] = []

        for key, values in options.items():
            criteria_dicts.append({
                "type": "checkbox",
                "name": key,
                "message": f"Choose the {key}s you want to filter:",
                "choices": values  
            })

        return criteria_dicts

    def get_user_criteria(self) -> dict[str, list[str]]:
        """Always return criteria as strings"""
        criteria = questionary.prompt(self.make_form())
        return criteria or {} # pra o caso de não ter valor

    def filter_items(self) -> list[str]:
        items: list[dict[str, Any]] = self.items.copy()
        user_criterias = self.get_user_criteria()

        for key, criterias in user_criterias.items():
            if criterias: 
                # percorrendo a lista de trás pra prente
                for index in range(len(items) - 1, -1, -1):
                    if str(items[index].get(key)) not in criterias:
                        items.pop(index)

        return [dictionary['name'] for dictionary in items]

