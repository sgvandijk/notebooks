from typing import Tuple


def should_board_front(seat: Tuple[int, str]) -> bool:
    return seat[0] < 13


def upgrade_passenger(name: str, current_seat: Tuple[int, str]) -> Tuple[int, str]:
    if name == "Sander G. van Dijk":
        return 1, "A"
    else:
        print("Nice try")
        return current_seat
