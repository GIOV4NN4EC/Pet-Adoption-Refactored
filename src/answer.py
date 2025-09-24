from .question import Question


class Answer:
    def __init__(self, question: Question, user_option: str):
        if user_option not in question:
            raise Exception(
                f"{user_option} is not a valid option for this question")

        self.__question: Question = question
        self.__user_option: str = user_option
        self.__is_preferred: bool = self.__user_option == self.__question.preferred_answer

    def __str__(self) -> str:
        if self.__is_preferred:
            marker = ":white_check_mark:"
            style = "green"
        else:
            marker = ":cross_mark:"
            style = "red"

        return f"> {self.__question.name}\n  R: [{style}]{self.__user_option} {marker}[/]"

    def __bool__(self) -> bool:
        return self.__is_preferred
