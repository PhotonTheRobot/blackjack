
#create the gambler configuration class based off the json in DefaultConfiguration.py. Use the same style as the shoe configuration class.
class GamblerConfiguration:
    """
    Class to represent the configuration of a gambler in a blackjack game.
    This class is used to set up the gambler with a specific bankroll and betting limits.
    """
    _trueCountChipValue = None
    _bankroll = None
        
    #Getters for the gambler configuration
    @property
    def Bankroll(self):
        return self._bankroll

    @property
    def BaseChipValue(self):
        return self._trueCountChipValue
    
    
    def __init__(self, gamblerConfiguration):
        self._bankroll = gamblerConfiguration['bankroll']
        self._trueCountChipValue = gamblerConfiguration['trueCountChipValue']
