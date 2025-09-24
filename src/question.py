class Question:
    def __init__(self, name: str, options: list[str], preferred_answer: str):
        if len(name) < 5:
            raise ValueError("question is too short")

        if name[-1] != "?":
            name = name + "?"

        self.__name: str = name
        self.__options: list[str] = options
        self.__preferred_answer: str = preferred_answer

    @property
    def name(self) -> str:
        return self.__name

    @property
    def options(self) -> list[str]:
        return self.__options

    @property
    def preferred_answer(self) -> str:
        return self.__preferred_answer

    def formatted_list(self) -> list[str]:
        question_info: list[str] = [f"> {self.__name}"]
        question_info.extend([f"    - {option}" for option in self.__options])

        return question_info

    def __iter__(self):
        return iter(self.__options)

    def __len__(self):
        return len(self.__options)

    def __str__(self) -> str:
        return f"{self.name} [{len(self)} options]"
