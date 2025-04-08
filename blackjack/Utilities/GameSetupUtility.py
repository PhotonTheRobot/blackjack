
from blackjack.Controllers.GameController import GameController
from blackjack.Models.Gambler import Gambler
from blackjack.Models.Dealer import Dealer
from blackjack.Models.Shoe import Shoe
from blackjack.Models.Configuration.GameConfiguration import GameConfiguration

def setup_game(config):
    """Set up the GameController class that runs the game from a configuration dictionary."""
    # Extract values from configuration. Note that this dict could grow and be stored/loaded from a
    # different source, so doing this to keep configuration flexible.
    
    # Create core components of the game: A Gambler, a Dealer, and a Shoe of cards.
    gamblerConfig = config['gambler']
    minBet = config['table']['minBet']
    gambler = Gambler(gamblerConfig, minBet)
    
    tableConfig = config['table']
    shoe = Shoe(tableConfig)
    
    dealer = Dealer()

    # Extract gameplay configuration values.
    gameplayConfig = config['gameplay']
    maxTurnsPerIteration = gameplayConfig['maxTurnsPerIteration']
    maxIterations = gameplayConfig['maxIterations']
    logLevel = gameplayConfig['logLevel']
    
    # Extract specific table configuration values.  
    penetration = tableConfig['penetration']
    maxBet = tableConfig['maxBet']
    baseChip = gamblerConfig['trueCountChipMultiplier']
    
    logLevel = gameplayConfig['logLevel']

    # Instantiate and return the central controller of the game.
    return GameController(gambler, dealer, shoe, penetration, minBet, maxBet, baseChip, maxTurnsPerIteration, maxIterations, logLevel)
