from typing import Any
import questionary


class Query:
    def __init__(self, items: list[dict[str, Any]]):
        self.items: list[dict[str, Any]] = items

    def get_options(self) -> dict[str, list[str]]:
        """Gets all options"""
        options: dict[str, list[str]] = {}

        for dictionary in self.items:
            for key, value in dictionary.items():
                if value is not None and key != "name":
                    value_str = str(value)
                    if key not in options:
                        options[key] = []
                    if value_str not in options[key]:
                        options[key].append(value_str)

        return options

    def make_form(self) -> list[dict[str, str | list]]:
        options = self.get_options()
        criteria_dicts: list[dict[str, str | list]] = []

        for key, values in options.items():
            sorted_values = sorted(values)
            
            choices = [f"[Include pets without {key}]"] + sorted_values
            
            criteria_dicts.append({
                "type": "checkbox",
                "name": key,
                "message": f"Choose the {key}s you want to filter (leave empty to skip):",
                "choices": choices
            })

        return criteria_dicts

    def get_user_criteria(self) -> dict[str, list[str]]:
        form = self.make_form()
        
        if not form:
            return {}
            
        criteria = questionary.prompt(form)
        return criteria or {}

    def filter_items(self) -> list[str]:
        user_criterias = self.get_user_criteria()
        
        active_criterias = {k: v for k, v in user_criterias.items() if v}
        
        if not active_criterias:
            return [item['name'] for item in self.items]
        
        filtered_items = []
        
        for item in self.items:
            matches_all = True
            
            for key, selected_values in active_criterias.items():
                include_none = f"[Include pets without {key}]" in selected_values
                
                actual_values = [v for v in selected_values if not v.startswith("[Include")]
                
                item_value = item.get(key)
                
                if item_value is None:
                    if not include_none:
                        matches_all = False
                        break
                else:
                    if actual_values and str(item_value) not in actual_values:
                        matches_all = False
                        break
            
            if matches_all:
                filtered_items.append(item['name'])
        
        return filtered_items
