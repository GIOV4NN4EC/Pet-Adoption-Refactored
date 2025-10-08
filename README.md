# Pet-Adoption-Refactored
Refactoring and implementation of Design Patterns in the [Pet Adoption App](https://github.com/wyvianvalenca/pet-adoption-OO).

## How to install?

### Clone the repository and go to the project folder:
```bash
git clone https://github.com/GIOV4NN4EC/Pet-Adoption-Refactored.git
cd Pet-Adoption-Refactored
```
### Virtual Envoirement
For this project, you can use a Virtual Envoirement, and here's how to create one and activate:
```bash
python -m venv venv
source venv/bin/activate
```
### External Libraries
We'll use a few external libraries that are already listed in requirements.txt, and here's how to install them:
```bash
pip install -r requirements.txt
```
### Run the main file
```bash
python main.py
```

## Requirements
- [OK] User Account Management: Users can create and manage their accounts;
- [OK] Pet Profile Management: Managing profiles for pets available for adoption;
- [OK] Shelter and Rescue Organization Profiles: Profiles for shelters and rescue organizations;
- [OK] Event Listing and Management: Listing events like adoption drives and fundraisers;
- [OK] Educational Resources: Providing resources on pet care and adoption;
- [OK] Success Stories and Testimonials: Sharing success stories and testimonials from adopters;
- [OK] Community Forum: A forum for adopters and pet lovers to share experiences and advice.
- [OK] Adoption Application Processing: Handling and processing adoption applications;
- [OK] Donation Processing: Facilitating donations to shelters and rescue organizations.
- [OK] Search and Filter Options: Enabling users to search and filter pets based on various criteria;

---

## Implemented Patterns
### Creational Patterns
- Factory Mode: `UserFactory`
- Protoype: `Form(Prototype)`
- Builder: `PetProfileBuilder`
### Behavioral Patterns
- State: `InReviewState`, `ApprovedState`, `DeniedState`
- Mediator: `AdoptionMediator`
- Observer: `AdopterObserver`, `ShelterObserver`


---

## Classes
### Event 
Shelter organized events (fundraisers, pet fairs, etc.)

- has:
    - location (Address)
    - date (Date)
    - status (str)
        - indicates if event has happened, has been cancelled or is in stand-by or in planning

- can:
    - update: change any info
    - cancel: change status to 'cancelled'
    - end: chage status to 'done'

---

### Donation
A money donation to a shelter

- has:
    - donor (Adopter)
    - receiver (Shelter)
    - ammount (float)
    - date (Date)

- can:
    - format: returns the donation's info in a pretty formatted way

---

### Form (Prototype)
Template for aplication (list of questions)  
Prototype for adoption forms

- has:
     - name (str)
     - questions (list[Question])
- can:
     - `clone()`: create a deep copy of a form with Prototype pattern
     - add or remove questions
     - formatted_list: formats all questions

---

### Question (Prototype)
Prototype for form questions

- has:
     - name (str)
     - options (list[str])
     - preferred_answer (str)
 - can:
     - `clone()`: duplicate a question while keeping its structure
     - formatted_list: formats the question and options in a list of strings

### Answer

- has:
    - question (Question)
    - user_option (str)
    - is_preferred (bool)

- can
    - format: returns the donation's info in a pretty formatted way

### Application
An Adopter's application to adopt a pet
Uses State pattern

- has:
    - applicant (Adopter)
    - pet (Pet)
    - answers (list[Answer])
    - score (str)
        - indicates the compatibility between the applicant's answers and the expected answers
    - state (ApplicationState)
         - can be `InReviewState`, `ApprovedState`, or `DeniedState`
    - feedback (str)

- can:
    - format: returns the questions, answers, score and status in a pretty formatted way
    - approve: changes state from `InReviewState` -> `ApprovedState`
    - deny: changes state from `InReviewState` -> `DeniedState` and records feedback
    - remain stable: if already approved or denied, further attempts to approve/deny keep the current state and prevent overwriting feedback

---

### ApplicationState
Abstract base class for an application's state

- can:
     - approve: defines how the application reacts when approved
     - deny: defines how the application reacts when denied
     - name: returns the state name ("approved", "denied", "in review")
 
---

### InReviewState
State for an application currently under review

- can:
     - approve: changes state to `ApprovedState`
     - deny: changes state to `DeniedState` and records feedback
     - name: returns `"in review"`

---

### ApprovedState
State for an application that was succesfully approved

- can:
     - approve: does nothing (already approved)
     - deny: does nothing (cannot be denied once approved)
     - name: returns `"approved"`

---

### DeniedState
State for an application that was denied

- can:
     - approve: does nothing (cannot be approved once denied)
     - deny: does nothing (already denied, prevents feedback overwrite)
     - name: returns `"denied"`

---

### Address 
Class for storing a structured address

- has:
    - street (str)
    - district (str)
    - number (str): can be "10", "11A", etc.
    - postal_code (int)

- can:
    - format: returns a pretty formatted address

---

### Profile
General informations for users and pets

- has:
    - name (str)
    - birth/open date (Date)
    - address (Adress)
    - description (str)

- can:
    - update_profile: change any attribute
    - format: returns all the profile's info in a pretty formatted way


---

### User

- has:
    - username (str)
    - profile (Profile)
    - allowed_post_types (list[str])
    - posts (list[Post])

- can:
    - login: returns User object
    - format: returns brief User description

---

### Adopter (User)
Inherits User's attributes and methods

- has:
    - donations (list[Donation])
    - applications (list[Aplication])

- can:
    - donate: donate to a shelter
    - apply: fill out form to adopt pet
      
---

### Shelter (User) 
Inherits User's attributes and methods.

Organizations that rescue pets and facilitate adoptions.

- has:
    - allowed_pet_types (list[str])
    - pets (list[Pet])
    - events (list[Event])

- can:
    - add_allowed_pet_type: add a new species to shelter's list
    - is_allowed(pet_type): indicates if Shelter accepts pet_type
    - approve_application: approve an application to adopt a pet, deny and provide feedback for all others and make applicant the pet's tutor
    - deny_application: deny an application

---

### Pet
Rescued animals

- has:
    - profile (Profile)
    - pet_type (str)
    - breed (str)
    - fur_color (str)
    - status (str)
        - rescued, in_treatment, available_for_adoption, adopted
    - form (Form)
        - questions for adoption application form
    - tutor (Adopter)

- can:
    - treat: change status to 'in_treatment'
    - make_available: change status to 'available_for_adoption'
    - add_template_question: add a question to application_template
    - [NEW] assign_form: assign a default form template for the pet
    - apply_to_adopt: fill the pet's form to apply for adoption

---

### Post
A social post

- has:
    - author (User)
    - post_type (str)
    - title (str)
    - content (str)
    - comments (list[Post])
    - likes (list[User])

- can:
    - update: change post's info
    - comment: add a comment to post
    - like: like the post
    - format: returns posts info in a pretty formatted way


---

### Query
A class for searching and filtering objects (pets, events, shelters, posts)

- has:
    - options: all available instances
    - criteria: all available criteria for filtering
    - filters: user selected filters
    - result: instances that  fit selected filters

- can:
    - search: find one specific object
    - filter: filter all objects based on various criteria
 
---

### UserFactory
Factory Method for users

- has:
     - static method: `create_user`
- can:
     - create users of type `adopter` or `shelter` without exposing their constructors
     - raise error if user type is unknown
 
---

### PetProfileBuilder
Builder for `PetProfile`

- has: 
     - step-by-step configuration methods:
          - `with_birth(date)`
          - `with_address(Address)`
          - `with_description(str)`
          - `with_breed(str)`
          - `with_color(str)`
- can:
     - construct a `PetProfile` object incrementally
     - allow flexible creation of pet profiles with optional attributes

---

### AdoptionMediator
Abstract Mediator for coordinating the adoption process

- can:
     - create_application: create a new application for a given pet and adopter
     - approve_application: approve a given application
     - deny_application: deny a given application with feedback
 
---

### ConcreteAdoptionMediator
Concrete implementation of the mediator pattern, centralizing communication between `Pet`, `Adopter`, `Shelter`, and `Application`

- has:
     - pets (dict[str, Pet])
     - adopters (dict[str, Adopter])
     - shelters (dict[str, Shelter])
     - applications (dict[str, Application])
 - can:
     - create_application:
          - validates pet and adopter
          - creates an `application`
          - updates pet's application count
     - approve_application:
          - validates pet and adopter
          - changes application's state to approved
          - assigns adopter as pet's tutor
          - updates pet status to adopted
     - deny_application:
          - chhanges application's state to denied
          - stores feedback

---

### ApplicationNotifier
Observer pattern implementation to update applicants and shelters about the adoption application proccess

- has:
    - observers: (dict[str, Observer])
- can:
    - attach new applicants to the observers list
    - detach applicants of the observers list
    - notify the applicants and shelters on the observers list


---

### AdoptionObserver
Observer pattern implementation to update the applicants/adopters about the application/adoption proccess

- has:
    - adopter(str)
    - pet(str)
    - status(str)
 
- can:
    - notify the applicant about the application proccess updates
 
---

### ShelterObserver
Observer pattern implementation to update the shelters about new adoption applications

- has:
    - shelter(str)
    - pet(str)
 
- can:
    - notify the shelter about new adoption applications
