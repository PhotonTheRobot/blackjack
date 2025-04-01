from copy import copy, deepcopy
import math
import numpy as np

from blackjack.models.Deck import Deck

class Shoe:
    #private vars
    _isLastHand = False
    _decks = []
    _totalCardsInDeck = 0
    _totalCardsDrawn = 0
    _startOfLastHand = 0
    _runningCount = 0
    _cards = [] 
    _cardLookup = {}
    
    #getters
    @property
    def IsLastHand(self):
        return self._isLastHand
    
    
    @property
    def DecksRemaining(self):
        return math.roof((self._totalCardsInDeck - self._totalCardsDrawn) / 52)    


    #constructor
    def __init__(self, num_decks, penetration):
        prototypicalDeck = Deck() 
        self._cardLookup = prototypicalDeck.CardLookup

        self.decks = [copy(prototypicalDeck) for _ in range(num_decks)]
        self._totalCardsInDeck = num_decks * 52
        self.startOfLastHand = self._totalCardsInDeck - ( penetration * 52 )        
        self._cards = np.zeros((self._totalCardsInDeck), dtype=int)  
        
        #Add every card from all of the decks into _cards numpy array
        index = 0
        for deck in self.decks:
            for cardIndex in deck.Cards:
                card = deck.Cards[cardIndex]
                #card.Id is the unique identifier for the card
                self._cards[cardIndex] = card.CardId
                index += 1

        self.ResetShoe()


    def ResetShoe(self):
        self._runningCount = 0
        self._totalCardsDrawn = 0
        self._isLastHand = False
        np.random.shuffle(self._cards) 


    def DealCard(self):

        if self._totalCardsDrawn >= self._startOfLastHand:
            self._isLastHand = True
        
        #pull a card from the front of the shoe
        cardId = self.cards[self._totalCardsDrawn]

        #return the card object from a hashtable lookup
        drawnCard = self.cardLookup[cardId]
        self._runningCount += drawnCard.AdvantagedPlayerValue
        self._totalCardsDrawn += 1

        return drawnCard        

