
from blackjack.Models.Hand import Hand
from blackjack.values.CardRank import CardRank
from blackjack.values.HandStatus import HandStatus

class DealerHand(Hand):
    @property
    def UpCard(self):
        return self._cards[0]

    def __init__(self, cards=[], status=None):
        super().__init__(cards, status)
        self._status = status if status else HandStatus.Pending


    def IsShowingAce(self):
        """Check whether the dealer is showing an ace."""
        return self.UpCard.Rank == CardRank.Ace

    def IsShowingFaceCard(self):
        """Check whether the dealer is showing a face card."""
        upCard = self.UpCard
        return upCard == CardRank.King or upCard == CardRank.Queen or upCard == CardRank.Jack or upCard == CardRank.Ten
