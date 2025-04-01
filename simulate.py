"""Script for analyzing how a strategy performs in repeated simulations of a set number of turns."""

import asyncio
from argparse import ArgumentParser

from blackjack.analytics.multi_game_analyzer import MultiGameAnalyzer
from blackjack.controllers.configuration import get_simulation_configuration
from blackjack.controllers.display_utils import clear, header
from blackjack.controllers.game_setup import setup_game
from blackjack.strategies import AdvancedPlayStrategy
from blackjack.strategies.SideBetStrategy import SideBetStrategy

STRATEGY_MAP = {
    'blackjack': AdvancedPlayStrategy,
    'sidebet': SideBetStrategy
}


async def worker(game):
    game.Play()
    return game.metric_tracker

async def main():
    # Command line args
    parser = ArgumentParser()
    parser.add_argument('-a', '--auto-wager', help='Initial Gambler auto-wager', type=float, default=15.0)
    parser.add_argument('-b', '--bankroll', help='Initial Gambler bankroll', type=float, default=10000.0)
    parser.add_argument('-c', '--concurrency', help='Number of game subprocesses to run simultaneously', type=int, default=4)
    parser.add_argument('-d', '--decks', help='Number of decks to play with', type=int, default=6)
    parser.add_argument('-p', '--penetration', help='Number of decks worth of penetration', type=float, default=1.0)
    parser.add_argument('-g', '--games', help='Number of games to simulate', type=int, default=1)
    parser.add_argument('-s', '--strategy', help='Name of the gameplay strategy to use', default='blackjack', choices=STRATEGY_MAP.keys())
    parser.add_argument('-t', '--turns', help='Max number of turns to play per game', type=int, default=1000)
    args = parser.parse_args()

    # Clear the terminal screen.
    clear()    
    # Get the requested gameplay strategy
    strategy = STRATEGY_MAP[args.strategy]

    # Load the game configuration (in this case, the 'simulation' configuration).
    configuration = get_simulation_configuration(args.bankroll, args.auto_wager, args.decks, args.penetration, strategy, args.turns)

    asyncGames =  []
    # Multiprocess game execution and collect MetricTrackers from each simulated game (with a progress bar!)

    for i in range(args.games):
        asyncGames.append(setup_game(configuration))
        
    taskResults = await asyncio.gather(
            #create an asyncio task for each game and run them in parallel
            *(worker(game) for game in asyncGames)
        )

    # Collect the results from each game and combine them into a single list of MetricTrackers.
    combinedResults = []
    for result in combinedResults:
        combinedResults.extend(result)

    # Analyze the results of the games
    print(header('ANALYTICS'))
    analyzer = MultiGameAnalyzer(combinedResults)
    analyzer.print_summary()
    analyzer.create_plots()


if __name__ == '__main__':
    # Run the main function in an asyncio event loop.
    asyncio.run(main())