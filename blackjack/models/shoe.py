import random
import math

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
        self.decks = [Deck(i) for i in range(num_decks)]
        self._totalCardsInDeck = num_decks * 52
        self.startOfLastHand = self._totalCardsInDeck - ( penetration * 52 )        
        self.cards = np.zeros((self._totalCardsInDeck), dtype=int)   
        
        cardIteration = 0
        for deck in self.decks:
            for card in deck.cards:                
                #fill numpy array with the count value of each card
                self.cardLookup[card.cardId] = card
                self.cards[cardIteration] = card.cardId
                cardIteration += 1
        
        self.ResetShoe()


    def ResetShoe(self):
        self._runningCount = 0
        self._totalCardsDrawn = 0
        self._isLastHand = False
        np.random.shuffle(self.cards) 


    def DealCard(self):

        if self._totalCardsDrawn >= self._startOfLastHand:
            self._isLastHand = True
        
        #pull a card from the front of the shoe
        cardId = self.cards[self._totalCardsDrawn]

        #return the card object from a hashtable lookup
        drawnCard = self.cardLookup[cardId]
        self._runningCount += drawnCard.ApValue
        self._totalCardsDrawn += 1

        return drawnCard        

