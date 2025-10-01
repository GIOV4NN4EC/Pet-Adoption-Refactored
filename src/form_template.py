from src.classes import Form

default_adoption_form = Form("Default Adoption Form")

default_adoption_form.add_question(
    "Why do you want to adopt this pet?",
    ["Companionship", "Gift", "Guard", "Other"],
    "Companionship"
)

default_adoption_form.add_question(
    "Do you live in a house or apartment?",
    ["House", "Apartment", "Other"],
    "House"
)

default_adoption_form.add_question(
    "How much time can you dedicate daily to your pet?",
    ["Less than 1 hour", "1-3 hours", "More than 3 hours"],
    "1-3 hours"
)

default_adoption_form.add_question(
    "Do you already have other pets?",
    ["Yes", "No"],
    "No"
)

default_adoption_form.add_question(
    "Are you financially able to cover food and veterinary costs?",
    ["Yes", "No"],
    "Yes"
)
