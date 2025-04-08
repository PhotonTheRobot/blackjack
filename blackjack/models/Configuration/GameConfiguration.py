#define a class for the game configuration that matches the json in DefaultConfiguration.py
from blackjack.Models.Configuration.GamblerConfiguration import GamblerConfiguration
from blackjack.Models.Configuration.GameConfiguration import GameConfiguration
from blackjack.Models.Configuration.GameplayConfiguration import GameplayConfiguration
from blackjack.Models.Configuration.TableConfiguration import ShoeConfiguration
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

_gambler = None
_shoe = None
_gameplay = None


@property
def Gambler(self):
    return _gambler

@property
def Shoe(self):
    return _shoe
    
@property
def Gameplay(self):
    return _gameplay


class GameConfiguration:
    def __init__(self, config):
        self._gambler = GamblerConfiguration(config['gambler'])
        
        self._shoe = ShoeConfiguration(config['shoe'])

        self._gameplay = GameplayConfiguration(config['gameplay'])
        
        