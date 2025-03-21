from blackjack.values.CardRanks import CardRank


class Dealer:
    _hand = None
    _name = 'Dealer'

    def __init__(self, hand=[]):
        self._hand = hand

    def UpCard(self):
        return self._hand[0]

    def IsShowingAce(self):
        """Check whether the dealer is showing an ace."""
        return self.UpCard() == CardRank.Ace

    def IsShowingFaceCard(self):
        """Check whether the dealer is showing a face card."""
        return self.UpCard() == CardRank.King or self.UpCard() == CardRank.Queen or self.UpCard() == CardRank.Jack or self.UpCard() == CardRank.Ten
    
    def DiscardHand(self):
        """Reset the dealer's hand."""
        self._hand = []
