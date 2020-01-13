def make_sound(animal: str) -> str:
    """Determine the sound an animal makes"""
    animal = _normalize(animal)
    if animal == "cat":
        return "meow"
    elif animal == "dog":
        return "woof"
    else:
        return "unknown"


def baby_name(animal: str) -> str:
    animal = _normalize(animal)
    if animal == "cat":
        return "kitten"
    elif animal == "dog":
        return "puppy"
    else:
        return "unknown"


def _normalize(animal: str) -> str:
    """Turn variations of animal names into standard form"""
    return animal.lower()