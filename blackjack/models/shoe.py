from copy import copy, deepcopy
import math
import numpy as np

from blackjack.Models.Deck import Deck

class Shoe:
    #private vars
    _isLastHand = False
    _decks = []
    _totalCardsInShoe = 0
    _totalCardsDrawn = 0
    _startOfLastHand = 0
    _runningCount = 0
    
    #An array of cards in the shoe. This is a numpy array of integers that represent the card Ids.
    _cardIds = np.array([], dtype=int) 
    #A hashtable of cards in the shoe. This is a dictionary that maps the card Id to the card object.
    _cardDictionary = {}
    
    #getters
    @property
    def IsLastHand(self):
        return self._isLastHand
    
    @property
    def RunningCount(self):
        return self._runningCount
    
    @property
    def TrueCount(self):
        if self.DecksRemaining > 0:
            trueCountFraction = self.RunningCount / self.DecksRemaining
            return math.floor(trueCountFraction)
        else:
            return 0
    
    @property
    def DecksRemaining(self):
        return math.ceil((self._totalCardsInShoe - self._totalCardsDrawn) / 52)    

    #constructor
    def __init__(self, tableConfig):
        """
        Initialize the Shoe with a number of decks and penetration level.
        The penetration level determines how many cards are left in the shoe before it is reshuffled.
        """
        numDecks = tableConfig['numberOfDecks']
        penetration = tableConfig['penetration']
        
        prototypicalDeck = Deck() 
        self._cardLookup = prototypicalDeck.CardLookup

        self.decks = [copy(prototypicalDeck) for _ in range(numDecks)]
        self._totalCardsInShoe = numDecks * 52
        self.startOfLastHand = self._totalCardsInShoe - ( penetration * 52 )        
        self._cardIds = np.full(self._totalCardsInShoe, -1, dtype=int)
        
        deckIndex = 0
        #Add every card from all of the decks into _cards numpy arra
        for deck in self.decks:
            cardIndex = 0
            deckAdjustment = deckIndex * 52
            
            for npCard in deck.Cards:
                cardId = npCard.item()

                #fill the private variable
                self._cardIds[cardIndex + deckAdjustment] = cardId
                cardIndex += 1
                
            deckIndex += 1

        self.ResetShoe()


    def ResetShoe(self):
        self._runningCount = 0
        self._totalCardsDrawn = 0
        self._isLastHand = False
        np.random.shuffle(self._cardIds) 


    def DealCard(self):

        if self._totalCardsDrawn >= self._startOfLastHand:
            self._isLastHand = True
        
        #pull a card from the front of the shoe
        cardId = self._cardIds[self._totalCardsDrawn]

        #return the card object from a hashtable lookup
        drawnCard = self._cardLookup[cardId]
        self._runningCount += drawnCard.AdvantagedPlayerValue
        self._totalCardsDrawn += 1

        return drawnCard  
    
    def DealMultipleCards(self, numCards):
        """
        Deal multiple cards from the shoe.
        :param numCards: The number of cards to deal.
        :return: A list of dealt cards.
        """
        cards = []
        for _ in range(numCards):
            cards.append(self.DealCard())
        return cards          