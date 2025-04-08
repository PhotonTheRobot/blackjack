import logging
import os

from pandas import read_csv
from blackjack.Controllers.CsvController import CsvController
from blackjack.values.PlayerAction import PlayerActions
from blackjack.values.Constants import Constants  # Import Constants

GLOBAL_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    
class AdvancedPlayStrategy():
    
    _csvController = None
    _logger = None

    
    
    #Empty init method to satisfy the abstract base class requirement.
    def __init__(self):
        super().__init__()
        self._csvController = CsvController()
        self._logger = logging.getLogger(__name__)
        self.split_df = self._load_df("default", 'split')
        self.soft_df = self._load_df("default", 'soft')
        self.hard_df = self._load_df("default", 'hard')

    @staticmethod
    def _load_df(strategy_name, csv_type):
        """Load a DataFrame from a CSV for determining actions."""
        csv_path = f"{GLOBAL_DIRECTORY}/csv/{strategy_name}/{csv_type}.csv"
        return read_csv(csv_path, index_col=0)
    
    def GetHandAction(self, hand, options):
        """Get the action to take on the hand ('Hit', 'Stand', etc.)"""
        # Get the dealer value by which to look up the correct action
        upCard = hand.UpCard
        column = self._csvController.GetCardFormat(upCard)

        # If splitting is an option, check if that action should be taken first.
        if PlayerActions.Split in options.values():
            row = hand.Cards[0].csv_format()
            if self.split_df.at[row, column] == Constants.SPLIT_STRING:  # Use Constants.SPLIT_STRING
                return PlayerActions.Split

        # Use the appropriate 'soft' or 'hard' hand DataFrame to decide which action should be taken.
        row = hand.CurrentTotal()
        if hand.IsSoft():
            action = self.soft_df.at[row, column]
        else:
            action = self.hard_df.at[row, column]

        # Handle the edge case where doubling is the recommended action, but the user doesn't have enough money to do so.
        if action == PlayerActions.Double:
            if PlayerActions.Double not in options.values():
                return PlayerActions.Hit
              
        return action
