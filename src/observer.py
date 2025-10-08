from abc import ABC, abstractmethod

class Observer(ABC):

    @abstractmethod
    def update(self):
        pass


class ApplicationNotifier:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)


class AdopterObserver(Observer):
    def __init__(self, adopter, pet, status: str):
        self.adopter = adopter
        self.pet = pet
        self.status = status

    #NOTIFYING THE APPLICANT ABOUT THE ADOPTION PROCCESS
    def update(self, message: str):
        print(f"The status of your application to adopt {self.pet.name} has changed to {self.status}")


class ShelterObserver(Observer):
    def __init__(self, shelter, pet):
        self.shelter = shelter
        self.pet = pet

    # NOTIFYING THE SHELTER ABOUT NEW APPLICATIONS
    def update(self, message: str):
        print(f"New application to adopt {self.pet.name}")
