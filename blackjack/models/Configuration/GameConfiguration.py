

from blackjack.Models.Configuration.GamblerConfiguration import GamblerConfiguration
from blackjack.Models.Configuration.GameplayConfiguration import GameplayConfiguration
from blackjack.Models.Configuration.ShoeConfiguration import ShoeConfiguration


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
        
        