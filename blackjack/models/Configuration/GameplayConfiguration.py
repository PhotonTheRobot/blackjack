class GameplayConfiguration:
    """
    Class to represent the configuration of gameplay in a blackjack game.
    This class is used to set up the game with specific rules and settings.
    """
    #create emtpy variables for the gameplay configuration
    _dealerStandsOnSoft17 = False
    _blackjackPayout = 1.5
    _insurancePayout = 2
    _surrenderPayout = 0.5
    _splitAllowed = True
    _doubleAfterSplit = True
    
        #Getters for the gameplay configuration
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
    def DoubleAfterSplit(self):
        return self._doubleAfterSplit
    
    @property
    def SplitAllowed(self):
        return self._splitAllowed
    
    def __init__(self, gameplayConfiguration):
        self._dealerStandsOnSoft17 = gameplayConfiguration['_dealerStandsOnSoft17']
        self._blackjackPayout = gameplayConfiguration['_blackjackPayout']
        self._insurancePayout = gameplayConfiguration['_insurancePayout']
        self._surrenderPayout = gameplayConfiguration['_surrenderPayout']
        self._doubleAfterSplit = gameplayConfiguration['_doubleAfterSplit']
        self._splitAllowed = gameplayConfiguration['_splitAllowed']
    
