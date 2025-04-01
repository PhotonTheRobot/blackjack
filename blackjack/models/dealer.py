from blackjack.models.Participant import Participant
from blackjack.values.CardRank import CardRank


class Dealer(Participant):
    _name = 'Dealer'
    _dealerHand = None

    def __init__(self, hands=[]):
        super().__init__(hands)    
        self._dealerHand = hands[0] if hands else None    

    def UpCard(self):
        return  self._dealerHand.Cards[0]

    def IsShowingAce(self):
        """Check whether the dealer is showing an ace."""
        return self.UpCard() == CardRank.Ace

    def IsShowingFaceCard(self):
        """Check whether the dealer is showing a face card."""
        return self.UpCard() == CardRank.King or self.UpCard() == CardRank.Queen or self.UpCard() == CardRank.Jack or self.UpCard() == CardRank.Ten
    
    def DiscardHand(self):
        """Reset the dealer's hand."""
        self._hand = []
