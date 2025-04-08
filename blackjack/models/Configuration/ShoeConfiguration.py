
class ShoeConfiguration():

    """
    Class to represent the configuration of a shoe in a blackjack game.
    This class is used to set up the shoe with a specific number of decks,
    penetration, and betting limits.
    """
    #create empty variables for the shoe configuration
    _numberOfDecks = 6
    _maxBet = 1000
    _minBet = 15
    _penetration = 1
    _trueCountChipValue = 25
    
    #Getters for the shoe configuration
    @property
    def NumberOfDecks(self):
        return self._numberOfDecks
    
    @property
    def Penetration(self):
        return self._penetration
    
    @property
    def MinBet(self):
        return self._minBet
    
    @property
    def MaxBet(self):
        return self._maxBet
    
    @property
    def BaseChipValue(self):
        return self._trueCountChipValue
    

    def __init__(self, shoeConfiguration):
        self._numberOfDecks = shoeConfiguration['numberOfDecks']
        self._penetration = shoeConfiguration['penetration']
        self._minBet = shoeConfiguration['minBet']
        self._maxBet = shoeConfiguration['maxBet']
        self._trueCountChipValue = shoeConfiguration['trueCountChipValue']