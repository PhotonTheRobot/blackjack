
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
        self._logger.debug("LoggingController initialized.")
        
    def LogCardValue(self, card):
        """Pretty print the card."""    
        match(card.Rank):
            case (1, 11):
                rankString += "Ace"
            case 10:
                rankString += "Ten"
            case 11:
                rankString += "Jack"
            case 12:
                rankString += "Queen"
            case 13:
                rankString += "King"
            case _:
                rankString += card.Rank
        
        match(card.Suit):
            case CardSuit.Hearts:
                suitString += self._heartsIcon
            case CardSuit.Diamonds:
                suitString += self._diamondsIcon
            case CardSuit.Clubs:
                suitString += self._clubsIcon
            case CardSuit.Spades:
                suitString += self._spadesIcon

        result = f'{rankString} of {suitString}'
        self._logger.debug(result)

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