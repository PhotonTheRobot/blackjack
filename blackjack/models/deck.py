from blackjack.models.Card import Card
import uuid
import numpy as np


from blackjack.values.CardSuits import CardNumbers, CardSuits

class Deck:

    _deckId = None
    _allSuits = [CardSuits.HEARTS, CardSuits.DIAMONDS, CardSuits.CLUBS, CardSuits.SPADES]
    _allRanks = [CardNumbers.ACE, CardNumbers.TWO, CardNumbers.THREE, CardNumbers.FOUR, CardNumbers.FIVE, CardNumbers.SIX, CardNumbers.SEVEN, CardNumbers.EIGHT, CardNumbers.NINE, CardNumbers.TEN, CardNumbers.JACK, CardNumbers.QUEEN, CardNumbers.KING]
    
    #make an empty 3d numpy array of 52 cards
    cards = np.zeros((4, 13), dtype=int)
    
    def __init__(self, deckNumber):
        self._deckId = uuid.uuid4()
        self._cards = np.zeros((4, 13), dtype=int)
        
        self._generateCards()


    def _generateCards(self):
        """Generate the cards for the deck."""
        for suit in self._allSuits:
            for rank in self._allRanks:
                self.allCards[suit][rank] = Card(suit, rank, self._deckId)

                    
                        
        
