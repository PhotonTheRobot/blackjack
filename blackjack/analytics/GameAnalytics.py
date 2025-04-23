from blackjack.values.HandOutcome import HandOutcome


class GameAnalytics:
    """Class for tracking game metrics for analytics purposes."""
    
    @property
    def PrimaryProfit(self):
        """Get the primary profit."""
        return self._loopProfit
    
    @property
    def SidebetProfit(self):
        """Get the sidebet profit."""
        return self._sidebetProfit
    
    
    def __init__(self):
        # Initial bankroll
        self._loopProfit = 0
        self._sidebetProfit = 0

    def AddToPrimaryProfit(self, profit):
        """Add to the profit."""
        self._loopProfit += profit
        
    def AddToSidebetProfit(self, profit):
        """Add to the profit."""
        self._sidebetProfit += profit