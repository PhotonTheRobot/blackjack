
from blackjack.GameController import GameController
from blackjack.models.Dealer import Dealer
from blackjack.models.Gambler import Gambler
from blackjack.models.Shoe import Shoe

def setup_game(config):
    """Set up the GameController class that runs the game from a configuration dictionary."""
    # Extract values from configuration. Note that this dict could grow and be stored/loaded from a
    # different source, so doing this to keep configuration flexible.
    name = config['gambler']['name']
    bankroll = config['gambler']['bankroll']
    auto_wager = config['gambler']['auto_wager']
    number_of_decks = config['shoe']['number_of_decks']
    strategy = config['gameplay']['strategy']
    verbose = config['gameplay']['verbose']
    max_turns = config['gameplay']['max_turns']
    penetration = config['shoe']['penetration']

    # Create core components of the game: A Gambler, a Dealer, and a Shoe of cards.
    gambler = Gambler(bankroll, auto_wager)
    dealer = Dealer()
    shoe = Shoe(number_of_decks, penetration)

    # Instantiate and return the central controller of the game.
    return GameController(gambler, dealer, shoe, strategy(), verbose=verbose, max_turns=max_turns)
