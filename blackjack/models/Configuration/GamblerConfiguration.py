#define a class for the game configuration that matches the json in DefaultConfiguration.py
from blackjack.Models.Configuration.GameConfiguration import GameConfiguration
from blackjack.Models.Participant import Participant
from blackjack.Models.Shoe import Shoe
from blackjack.Models.Dealer import Dealer
from blackjack.Models.Gambler import Gambler
from blackjack.Models.Exceptions.InsufficientBankrollException import InsufficientBankrollException
from blackjack.Models.Exceptions.OverdraftException import OverdraftException
from blackjack.Models.Hand import Hand
from blackjack.Models.Card import Card
from blackjack.values.CardRank import CardRank
from blackjack.values.CardSuit import CardSuit
from blackjack.values.HandStatus import HandStatus
from blackjack.Models.Configuration.TableConfiguration import ShoeConfiguration

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
