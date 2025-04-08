from blackjack.values.PlayerAction import PlayerActions
from blackjack.values.Constants import Constants  # Import Constants

class AdvancedPlayStrategy():
    #Empty init method to satisfy the abstract base class requirement.
    def __init__(self):
        super().__init__()

    def GetHandAction(self, hand, options, dealer_upcard):
        """Get the action to take on the hand ('Hit', 'Stand', etc.)"""
        # Get the dealer value by which to look up the correct action
        column = dealer_upcard.csv_format()

        # If splitting is an option, check if that action should be taken first.
        if PlayerActions.Split in options.values():
            row = hand.cards[0].csv_format()
            if self.split_df.at[row, column] == Constants.SPLIT_STRING:  # Use Constants.SPLIT_STRING
                return PlayerActions.Split

        # Use the appropriate 'soft' or 'hard' hand DataFrame to decide which action should be taken.
        row = hand.FinalTotal()
        if hand.IsSoft():
            action = self.soft_df.at[row, column]
        else:
            action = self.hard_df.at[row, column]

        # Handle the edge case where doubling is the recommended action, but the user doesn't have enough money to do so.
        if action == PlayerActions.Double:
            if PlayerActions.Double not in options.values():
                return PlayerActions.Hit
              
        return action
