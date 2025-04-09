
#Participant class
class Participant:
    """Base class for all participants in the game."""
    _hands = []
    
    @property
    def Hands(self):
        return self._hands

    @property
    def FirstHand (self):
        if self._hands == []:
            return []
        else:
            return self._hands[0]

    def __init__(self, hands=[]):
        self._hands = hands

    def Discard(self):
        """Empty the hand."""
        cardsToDiscard = []
        for hand in self._hands:
            cardsToDiscard += hand.Discard()
        cardsToDiscard = self._hands
        self._hands = []
        
    def GetAllHands(self):
        """Get all hands."""
        return self._hands

    def GetHand(self, handNumber):
        """Helper method for action that happens on the initial hand dealt to the gambler."""
        return self._hands[handNumber]