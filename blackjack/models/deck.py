from blackjack.Models.Card import Card
import uuid
import numpy as np
from blackjack.values.CardRank import CardRank
from blackjack.values.CardSuit import CardSuit

#Deck class
class Deck:
    _allSuits = [CardSuit.Hearts, CardSuit.Diamonds, CardSuit.Clubs, CardSuit.Spades]
    _allRanks = [CardRank.Ace, CardRank.Two, CardRank.Three, CardRank.Four, CardRank.Five,
                 CardRank.Six, CardRank.Seven, CardRank.Eight, CardRank.Nine, CardRank.Ten,
                 CardRank.Jack, CardRank.Queen, CardRank.King]
    
    _cardIds = []
    _cardLookup = {}
    
    
    @property
    def CardIds(self):
        return self._cardIds
    
    @property
    def CardLookup(self):
        return self._cardLookup
    
    
    #constructor
    def __init__(self):
        self._GenerateCards()


    def _GenerateCards(self):
        cardId = 1
        
        """Generate the cards for the deck."""
        for suit in self._allSuits:
            for rank in self._allRanks:
                # Starting at Rank-2 because the lowest card value is 2
                self._cardLookup[cardId - 1] = Card(cardId, suit, rank)
                self._cardIds.append(cardId)
                cardId += 1