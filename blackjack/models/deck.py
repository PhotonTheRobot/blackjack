from blackjack.models.Card import Card
import uuid
import numpy as np
from blackjack.values.CardRank import CardRank
from blackjack.values.CardSuit import CardSuit

class Deck:

    _deckId = None
    _allSuits = [CardSuit.Hearts, CardSuit.Diamonds, CardSuit.Clubs, CardSuit.Spades]
    _allRanks = [CardRank.Ace, CardRank.Two, CardRank.Three, CardRank.Four, CardRank.Five,
                 CardRank.Six, CardRank.Seven, CardRank.Eight, CardRank.Nine, CardRank.Ten,
                 CardRank.Jack, CardRank.Queen, CardRank.King]
    _cards = np.zeros((4, 13), dtype=int)
    
    @property
    def Cards(self):
        return self._cards
    
    #constructor
    def __init__(self, deckId):
        self._deckId = deckId
        self._generateCards()


    def _generateCards(self):
        """Generate the cards for the deck."""
        for suit in self._allSuits:
            for rank in self._allRanks:
                # Starting at Rank-2 because the lowest card value is 2
                self._cards[suit-1][rank-2] = Card(suit, rank, self._deckId)

                    
                        
        
