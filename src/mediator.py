from src.classes import Pet, Adopter, Shelter, Application

class AdoptionMediator:
    def create_application(self, applicant: str, pet: str, answers: list[str]) -> Application:
        raise NotImplementedError
    
    def approve_application(self, application: Application) -> None:
        raise NotImplementedError
    
    def deny_application(self, application: Application, feedback: str) -> None:
        raise NotImplementedError


class ConcreteAdoptionMediator(AdoptionMediator):
    def __init__(self):
        self.pets = Pet.data
        self.adopters = Adopter.data
        self.shelters = Shelter.data
        self.applications = Application.data

    def create_application(self, applicant: str, pet: str, answers: list[str]):
        pet_obj = self.pets.get(pet)
        adopter = self.adopters.get(applicant)
        
        if not pet_obj or not adopter:
            raise ValueError("Pet or adopter not found!")
        
        # CREATING THE APPLICATION
        app = Application(applicant, pet, pet_obj.form, answers)
        # UPDATING PET
        pet_obj.add_application()
        
        return app
    
    def approve_application(self, application: Application):
        pet_obj = self.pets.get(application.pet)
        adopter = self.adopters.get(application.applicant)

        if not pet_obj or not adopter:
            raise ValueError("Pet or adopter not found")
        
        application.approve()
        pet_obj.tutor = adopter
        pet_obj.was_adopted()

        print(f"{adopter.name}'s application to adopt {pet_obj.profile.name} APPROVED!\n")
        print("\nThis means all other applications must be denied. Let's give the other applicants some feedback!\n")

    def deny_application(self, application: Application, feedback: str = "") -> None:
        application.deny(feedback)
