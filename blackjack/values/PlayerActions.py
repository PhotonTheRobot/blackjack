from enum import Enum

class PlayerActions(Enum):
    Stay = 0
    Hit = 1
    Double = 2
    Split = 3
    Surrender = 4
    BuyInsurance = 5
    