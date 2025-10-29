from abc import ABC, abstractmethod

class FeedbackSender(ABC):
    @abstractmethod
    def send_feedback(self, adopter: str, pet: str, feedback: str):
        pass

# Printa o feedback com a formatação desejada no terminal
class ConsoleFeedbackAdapter(FeedbackSender):
    def send_feedback(self, adopter: str, pet: str, feedback: str):
        print(f"[Console] Feedback to {adopter} about {pet}: {feedback}")


# Registra o feedback em um arquivo .txt
class FileFeedbackAdapter(FeedbackSender):
    def send_feedback(self, adopter: str, pet: str, feedback: str):
        with open("feedback_log.txt", "a") as f:
            f.write(f"{adopter} - {pet}: {feedback}\n")
