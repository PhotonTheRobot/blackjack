
class Card:
    #private vars
    _cardId = None
    _suit = None
    _rank = 0
    _apValue = 0
    _countValue = 0

    def __init__(self, cardId, suit, rank):
        self._cardId = cardId
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
        
    def PrettyPrint(self, card):
        """Pretty print the card."""
        cardString = ""
        
        match(card.Value):
            case (1, 11):
                cardString += "Ace"
            case 10:
                cardString += "Ten"
            case 11:
                cardString += "Jack"
            case 12:
                cardString += "Queen"
            case 13:
                cardString += "King"
            case _:
                cardString += card.Rank
        
        match(card.Suit):
            case 0:
                cardString += " of Hearts"
            case 1:
                cardString += " of Diamonds"
            case 2:
                cardString += " of Clubs"
            case 3:
                cardString += " of Spades"
        
        
        
        if card.Value < 10:
            cardString += str(card.Value)
        
            return str(self._countValue)
        return f"{self._rank} of {self._suit}"
