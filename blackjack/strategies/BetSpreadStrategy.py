
class BetSpreadStrategy():

    _minBet = 0
    _maxBet = 0 
    _trueCountChipValue = 0

    def __init__(self, minBet, maxBet, trueCountChipValue):
        self._minBet = minBet
        self._maxBet = maxBet
        self._trueCountChipValue = trueCountChipValue

    def GetBidValue(self, shoe):
        """
        Get the bet value based on the current running count and the shoe.
        :param shoe: The current shoe being used.
        :return: The bet value.
        """
        # Calculate the bet value based on the running count and the shoe.
        if shoe.RunningCount > 0:
            
            trueCount = shoe.TrueCount
            if trueCount  > 6:
                trueCount = 6
            
            handBet = trueCount * self._trueCountChipValue
            if handBet > self._maxBet:
                return self._maxBet
            return 
        else:
            return self._minBet
