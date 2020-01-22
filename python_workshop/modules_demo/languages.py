def hello(language: str) -> str:
    if language == "Dutch":
        return "Hallo"
    elif language == "French":
        return "Bonjour"
    else:
        return "Hello"


def detect_language(text: str) -> str:
    for language in ["Dutch", "French", "English"]:
        if hello(language) == text:
            return language


# if __name__ == "__main__":
print(f"'Bonjour' is: {detect_language('Bonjour')}")
