def is_safe_for_hand_luggage(item: str) -> bool:
    return not (
            item == "fireworks"
            or (
                    "knive" in item
                    and item != "kniveholder"
            )
            or item == "vodka"
    )


def should_take_off(item: str) -> bool:
    return item in ["belt", "coat", "boots"]
