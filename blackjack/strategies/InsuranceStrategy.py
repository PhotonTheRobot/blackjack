
class InsuranceStrategy():

    _minimumTrueValue = None

    def __init__(self, minimumTrueValue = 3):
        self._minimumTrueValue = minimumTrueValue

    def WantsInsurance(self, trueCount, dealerHand, gambler):
        """
        Check if the player should buy insurance based on the true count and dealer's hand.
        """
        if dealerHand.IsShowingAce() and trueCount >= self._minimumTrueValue:
            return True
        
        return False
        