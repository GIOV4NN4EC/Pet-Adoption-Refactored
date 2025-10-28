import time
from src.mediator import ConcreteAdoptionMediator
from rich.console import Console

# FACADE PATTERN
class AdoptionFacade:

    def __init__(self):
        self.console = Console()
        self.mediator = ConcreteAdoptionMediator()

    def process_application(self, application):
        pet_name = application.pet
        adopter = application.applicant
        score = application.score
        status = application.state

        self.console.print(f"\n[bold]Processing adoption application...[/]")
        self.console.print(f"> Applicant: {adopter}")
        self.console.print(f"> Pet: {pet_name}")
        self.console.print(f"> Compatibility score: {score:.2f}\n")
        time.sleep(3)

        self.mediator.approve_application(application)
