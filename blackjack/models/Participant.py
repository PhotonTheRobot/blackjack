from blackjack.models.Hand import Hand
from blackjack.models.exceptions.InsufficientBankrollException import InsufficientBankrollException
from blackjack.models.exceptions.OverdraftException import OverdraftException


class Participant:
    """Base class for all participants in the game."""
    _hands = []
    
    @property
    def Hands(self):
        return self._hands


    def __init__(self, hands=[]):
        self._hands = hands

    def DiscardHands(self):
        """Empty the hand."""
        self._hands = []

    def GetHand(self, handNumber):
        """Helper method for action that happens on the initial hand dealt to the gambler."""
        return self._hands[handNumber]