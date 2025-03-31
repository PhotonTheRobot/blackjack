
class Card:
    #private vars
    _cardId = None
    _suit = None
    _rank = 0
    _apValue = 0
    _countValue = 0

    def __init__(self, suit, rank, deckId):
        self._cardId = rank + (deckId * 100) #unique card id, influenced by deck id
        self._suit = suit
        self._rank = rank
        
        if rank <= 6:
            self._apValue = 1
        elif rank >= 10:
            self._apValue = -1
            
        if rank < 10:
            self._countValue = (rank)
        elif rank >= 10 and rank <= 13:
            self._countValue = (10)
        else: #ace
            self._countValue = (1, 11)

    #getters
    @property
    def CardId(self):
        return self._cardId

    @property
    def Suit(self):
        return self._suit
    
    @property
    def Rank(self):
        return self._rank
    
    @property
    def CountValue(self):
        return self._countValue
    
    @property
    def AdvantagedPlayerValue(self):
        return self._apValue

    def GetCsvFormat(self):
        """String representation of the card for Strategy CSVs."""
        if self.IsAce():
            return 'A'
        else:
            return str(self._countValue)
