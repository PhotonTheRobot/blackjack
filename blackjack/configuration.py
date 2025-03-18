from blackjack.strategies.user_input_strategy import UserInputStrategy

def get_simulation_configuration(bankroll, auto_wager, number_of_decks, penetration, strategy, max_turns):
    """Get game configuration data for the simulation game mode."""
    return {
        'gambler': {
            'name': 'Gambler',
            'bankroll': bankroll,
            'auto_wager': auto_wager
        },
        'shoe': {
            'number_of_decks': number_of_decks,
            'penetration': penetration
        },
        'gameplay': {
            'strategy': strategy,
            'verbose': False,
            'max_turns': max_turns
        }
    }
