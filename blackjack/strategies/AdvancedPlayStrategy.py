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
        
        dataFrame = read_csv(csv_path, index_col=0)
        return dataFrame
    
    def GetHandAction(self, gamblerHand, options, dealerUpcard):
        """Get the action to take on the hand ('Hit', 'Stand', etc.)"""
        formattedUpcard = self._csvController.GetCardFormat(dealerUpcard)

        # If splitting is an option, check if that action should be taken first.
        if PlayerActions.Split in options.values():
            row = gamblerHand.Cards[0].Rank
            column = dealerUpcard.Rank
            if self.split_df.at[row, column] == Constants.SPLIT_STRING:  # Use Constants.SPLIT_STRING
                return PlayerActions.Split

        # Use the appropriate 'soft' or 'hard' hand DataFrame to decide which action should be taken.
        gamblerTotalCount = gamblerHand.CurrentTotal()
        
        if gamblerHand.IsSoft():
            action = self._GetAction(self.soft_df, gamblerTotalCount, formattedUpcard)
        else:
            action = self._GetAction(self.hard_df, gamblerTotalCount, formattedUpcard)

        # Handle the edge case where doubling is the recommended action, but the user doesn't have enough money to do so.
        if action == PlayerActions.Double:
            if PlayerActions.Double not in options.values():
                return PlayerActions.Hit
              
        return action
    
    
    def _GetAction(self, dataframe, playerValue, dealerValue):
        """Get the value from the DataFrame."""
        result = dataframe.at[playerValue, str(dealerValue)]
        
        match result:
            case Constants.Hit:
                value = PlayerActions.Hit
            case Constants.Stand:
                value = PlayerActions.Stand
            case Constants.Double:
                value = PlayerActions.Double
            case Constants.Split:
                value = PlayerActions.Split
            case Constants.Surrender:
                value = PlayerActions.Surrender
            case _:
                raise ValueError(f"Unknown action: {result}")
            
        return value
        