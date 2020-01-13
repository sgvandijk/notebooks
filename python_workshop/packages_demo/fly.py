from airport.security import is_safe_for_hand_luggage
from airport.gate import upgrade_passenger

print(f"Can I take an umbrella?   {'yes' if is_safe_for_hand_luggage('umbrella') else 'no'}")
print(f"Can I take a steak knive? {'yes' if is_safe_for_hand_luggage('steak knive') else 'no'}")

best_seat = upgrade_passenger("Sander van Dijk", (22, "F"))
print(best_seat)