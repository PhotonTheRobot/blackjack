 
class DiscardTray():

    def __init__(self):
        self._discardedCardIds = []


    def AddCards(self, cards):
        """Discard a list of cards."""
        for card in cards:
            self._discardedCardIds.append(card.CardId)


    def EmptyTray(self):
        """Remove all cards from the discard tray."""
        cardsToShuffle = self._discardedCardIds
        self._discardedCardIds = []
        return cardsToShuffle