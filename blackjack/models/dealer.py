from blackjack.Models.Participant import Participant
from blackjack.values.CardRank import CardRank


class Dealer(Participant):
    _name = 'Dealer'

    @property
    def Hand(self):
        return self._hands[0] if self._hands else []
    
    def __init__(self, hands=[]):
        super().__init__(hands)    

 