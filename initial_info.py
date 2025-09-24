from datetime import date
from src.address import Address
from src.adopter import Adopter
from src.application import Application
from src.donation import Donation
from src.event import Event
from src.pet import Pet
from src.post import Post
from src.shelter import Shelter


def create_data():
    # create users
    a1 = Adopter("wgcv", "Wyvian Valenca")
    a2 = Adopter("ybss", "Ycaro Sales")

    s1 = Shelter("csf", "Casa Sao Franscisco")
    s2 = Shelter("rh", "Reptile House")
    s3 = Shelter("k9s", "K9s")

    # update shelters
    s1.add_allowed_pet_type("dog")
    s2.add_allowed_pet_type("turtle")
    s3.add_allowed_pet_type("dog")

    s1.profile.birth = date(2010, 10, 10)
    s2.profile.birth = date(2020, 10, 10)
    s3.profile.birth = date(2024, 10, 12)

    s1.profile.address = Address(
        "Rua Maria Sampaio", "Feitosa", "704", 123654, "Maceio", "Alagoas")
    s2.profile.address = Address(
        "Av. Fernandes Lima", "Farol", "704", 123654, "Maceio", "Alagoas")
    s3.profile.address = Address(
        "Av. Mucio Uchoa Cavalcanti", "Engenho do Meio", "S/N", 50730285,
        "Recife", "Pernambuco")

    s1.profile.description = "Inspired by the compassion of Saint Francis of Assisi, the patron saint of animals, Casa São Francisco is a sanctuary for abandoned, neglected, and homeless dogs and cats."
    s2.profile.description = "Reptile House is a specialized rescue dedicated to the welfare of reptiles and exotic animals."
    s3.profile.description = "K9s is a dynamic, dog-focused rescue with a clear mission: to transform the lives of canines in need."

    # create pets
    p1 = Pet("shiro", s1.username, "dog")
    p2 = Pet("becky", s1.username, "dog")
    p3 = Pet("jack", s2.username, "turtle")

    # update pets' profiles
    p1.profile.birth = date(2021, 7, 20)
    p1.profile.breed = "labrador"
    p1.profile.color = "white"

    p2.profile.birth = date(2017, 10, 10)
    p2.profile.breed = "chow chow"
    p2.profile.color = "light brown"

    p3.profile.birth = date(2024, 6, 1)
    p3.profile.breed = "sea turtle"

    p1.add_template_question("How many walks can you take him on daily?",
                             ["0", "1", "2 or more"], "2 or more")

    p1.add_template_question("Are you severely affected by loud barking?",
                             ["Yes", "No"], "No")

    p1.add_template_question("How many hours will he be left alone?",
                             ["10h+", "8h", "6h", "4h or less"], "4h or less")

    ap1 = Application(a1.username, p1.profile.name, p1.form,
                      ["Yes", "2 or more", "No", "10h+"])
    ap2 = Application(a2.username, p1.profile.name, p1.form,
                      ["Yes", "2 or more", "No", "4h or less"])
    ap3 = Application(a1.username, p2.profile.name, p2.form, ["Yes"])
    ap4 = Application(a1.username, p3.profile.name, p2.form, ["Yes"])

    post1 = Post(s1, "educational",
                 "The Decompression Period: Giving Your New Pet Time to Adjust", """
Bringing a new pet home is an exciting time, but it's crucial to remember the **"3-3-3 Rule"** for rescue animals. This guideline helps you set realistic expectations for their adjustment period.

### The 3-3-3 Rule:
- **First 3 Days:** Your new pet will likely feel overwhelmed and scared.
    - They are not yet comfortable enough to be themselves. Don't be surprised if they hide or don't eat much.
- **First 3 Weeks:** Your pet is starting to settle in and learn your routine.
    - Their personality will begin to emerge as they realize they are in a safe and stable environment.
- **First 3 Months:** Your pet now feels at home and has built trust with your family.
    - This is when you'll see their true personality, and a real bond has been established.

***
*Patience during this time is the key to building a strong, lifelong foundation of trust.* """)

    post2 = Post(s2, "forum", "Volunteers Needed for Our Upcoming 'Clear the Kennel' Adoption Drive!", """
Hello, pet-loving community! Sunny Paws Shelter is hosting our annual **"Clear the Kennels"** adoption event in two weeks, and we're looking for enthusiastic volunteers to help make the day a success.

We need help with tasks like:
- Walking dogs and supervising play areas
- Managing the kitten playpen
- Talking to potential adopters about our amazing animals
- Assisting with the information and sign-up desk

If you're available to lend a hand and want to help our residents find their forever homes, please let us know in the comments! """)

    d1 = Donation(a1.username, s1.username, 100.00, date.today())
    d2 = Donation(a1.username, s2.username, 120.00, date.today())

    e1 = Event("fundraiser", date(2025, 10, 10), Address(
        "Av. Fernandes Lima", "Farol", "123456", 123456, "Maceio", "Alagoas"),
        s1.username)

    e1 = Event("fundraiser 2", date(2025, 12, 10), Address(
        "Av. Fernandes Lima", "Farol", "123456", 123456, "Maceio", "Alagoas"),
        s2.username)
