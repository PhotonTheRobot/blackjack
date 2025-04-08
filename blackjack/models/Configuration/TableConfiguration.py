#define class for the shoe configuration that matches the json in DefaultConfiguration.py

from blackjack.Models.Configuration.GameConfiguration import GameConfiguration  

_numberOfDecks = 6
_penetration = 1
_minBet = 15
_maxBet = 1000
_trueCountChipValue = 25

class TableConfiguration():

    """
    Class to represent the configuration of a shoe in a blackjack game.
    This class is used to set up the shoe with a specific number of decks,
    penetration, and betting limits.
    """
    #create empty variables for the shoe configuration
    _numberOfDecks = None
    _penetration = None
    _minBet = None
    _maxBet = None
    _dealerStandsOnSoft17 = None
    _doubleAfterSplitAllowed = None
    _maximumSplitsAllowed = None
    _surrenderAllowed = None
    _blackjackPayout = None
    _insurancePayout = None
    _doublePayout = None
    _surrenderPayout = None

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
    
    @property
    def DealerStandsOnSoft17(self):
        return self._dealerStandsOnSoft17
    
    @property
    def BlackjackPayout(self):
        return self._blackjackPayout
    
    @property
    def InsurancePayout(self):
        return self._insurancePayout
    
    @property
    def SurrenderPayout(self):
        return self._surrenderPayout
    
    @property
    def DoubleAfterSplitAllowed(self):
        return self._doubleAfterSplitAllowed
    
    @property
    def MaximumSplitsAllowed(self):
        return self._maximumSplitsAllowed
    
    @property
    def SurrenderAllowed(self):
        return self._surrenderAllowed

    @property
    def DoublePayout(self):
        return self._doublePayout
    
    @property
    def BlackjackPayout(self):
        return self._blackjackPayout
    
    @property
    def InsurancePayout(self):
        return self._insurancePayout
    
    @property
    def SurrenderPayout(self):
        return self._surrenderPayout
    

    def __init__(self, shoeConfiguration):
        self._numberOfDecks = shoeConfiguration['numberOfDecks']
        self._penetration = shoeConfiguration['penetration']
        self._minBet = shoeConfiguration['minBet']
        self._maxBet = shoeConfiguration['maxBet']
        self._trueCountChipValue = shoeConfiguration['trueCountChipValue']
        self._dealerStandsOnSoft17 = shoeConfiguration['dealerStandsOnSoft17']
        self._doubleAfterSplitAllowed = shoeConfiguration['doubleAfterSplitAllowed']
        self._maximumSplitsAllowed = shoeConfiguration['maximumSplitsAllowed']
        self._surrenderAllowed = shoeConfiguration['surrenderAllowed']
        self._blackjackPayout = shoeConfiguration['blackjackPayout']
        self._insurancePayout = shoeConfiguration['insurancePayout']
        self._doublePayout = shoeConfiguration['doublePayout']
        self._surrenderPayout = shoeConfiguration['surrenderPayout']
        