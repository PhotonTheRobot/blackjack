 
import numpy as np


class DiscardTray():

    def __init__(self):
        self._discardedCardIds = []


    def AddCards(self, cardIds):
        """Discard a list of cards."""
        for cardId in cardIds:
            self._discardedCardIds.append(cardId)


    def EmptyTray(self):
        """Remove all cards from the discard tray."""
        cardsToShuffle = self._discardedCardIds
        self._discardedCardIds = []
        return cardsToShuffle