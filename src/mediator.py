from src.classes import Pet, Adopter, Shelter, Application
from src.ui.name_validator import NameValidator
import questionary

from src.observer import AdopterObserver, ShelterObserver, ApplicationNotifier
from src.feedback_adapter import ConsoleFeedbackAdapter

class AdoptionMediator:
    def create_application(self, applicant: str, pet: str, answers: list[str]) -> Application:
        raise NotImplementedError
    
    def approve_application(self, application: Application) -> None:
        raise NotImplementedError
    
    def deny_application(self, application: Application, feedback: str) -> None:
        raise NotImplementedError


class ConcreteAdoptionMediator(AdoptionMediator, AdopterObserver):
    def __init__(self):
        self.pets = Pet.data
        self.adopters = Adopter.data
        self.shelters = Shelter.data
        self.applications = Application.data
        self.notifier = ApplicationNotifier()
        #ADAPTER PATTERN
        self.feedback_sender = ConsoleFeedbackAdapter()

    def create_application(self, applicant: str, pet: str, answers: list[str]):
        pet_obj = self.pets.get(pet)
        adopter = self.adopters.get(applicant)
        
        if not pet_obj or not adopter:
            raise ValueError("Pet or adopter not found!")
        
        # CREATING THE APPLICATION
        app = Application(applicant, pet, pet_obj.form, answers)

        # UPDATING PET
        pet_obj.add_application()

        # NOTIFYING SHELTER
        adopter_obs = AdopterObserver(adopter, pet_obj, app.status)
        shelter_obs = ShelterObserver(pet_obj.shelter, pet_obj)

        self.notifier.attach(adopter_obs)
        self.notifier.attach(shelter_obs)
        self.notifier.notify(f"New application to {pet_obj.profile.name}. User: {adopter.profile.name}")
        
        
        return app
    
    def approve_application(self, application: Application):
        pet_obj = self.pets.get(application.pet)
        adopter = self.adopters.get(application.applicant)

        if not pet_obj or not adopter:
            raise ValueError("Pet or adopter not found")
        
        application.approve()
        pet_obj.tutor = adopter
        pet_obj.was_adopted()

        self.notifier.notify(f"Your application to adopt {pet_obj.profile.name} was Approved! Congratulations!")
        
        print(f"{adopter.profile.name}'s application to adopt {pet_obj.profile.name} APPROVED!\n")
        print("\nThis means all other applications must be denied. Let's give the other applicants some feedback!\n")


    def deny_application(self, application: Application, feedback: str = "") -> None:
        application.deny(feedback)

        self.feedback_sender.send_feedback(application.applicant, application.pet, feedback)

        #OLD CODE WITHOUT IMPLEMENTING ADAPTER PATTERN
        """pet_obj = self.pets.get(application.pet)
        adopter = self.adopters.get(application.applicant)

        if pet_obj and adopter:
            self.notifier.notify(f"Your application to adopt {pet_obj.profile.name} was denied. \n{feedback}")"""
