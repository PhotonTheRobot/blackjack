
from blackjack.values.CardSuit import CardSuit


class LoggingController:
    #private vars
    _heartsIcon = "♥️"
    _diamondsIcon = "♦️"
    _clubsIcon = "♣️"
    _spadesIcon = "♠️"
    
    _logger = None

    def __init__(self, logger):
        self._logger = logger

    def GetMoneyFormat(self, money):
        """Format a monetary value as a string."""
        return "${:0,.2f}".format(money).replace('$-', '-$')

    def GetPercentFormat(self, percent):
        """Format a percent value as a string."""
        return "{0:+.2f}%".format(percent)

    def GetPercentageValue(self, numerator, denominator):
        """Get a percentage value through division, handling zero division errors."""
        try:
            return numerator / denominator * 100.0
        except ZeroDivisionError:
            return 0.0