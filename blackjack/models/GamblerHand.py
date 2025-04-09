from blackjack.Models.Hand import Hand
from blackjack.values.HandStatus import HandStatus

#GamblerHand class
class GamblerHand(Hand):
    _wager = 0
    _insurance = 0
    _handNumber = 0
    _earnings = 0
    _outcome = None
    
    @property
    def Earnings(self):
        """Get the summed earnings of the hand."""
        return self._earnings
    @Earnings.setter
    def Earnings(self, value):
        """Set the summed earnings of the hand."""
        self._earnings = value
    
    @property
    def Outcome(self):
        """Get the outcome of the hand."""
        return self._outcome
    @Outcome.setter
    def Outcome(self, value):
        """Set the outcome of the hand."""
        self._outcome = value
    
    
    def __init__(self, cards=None, status=HandStatus.Pending, wager=0, insurance=0, handNumber=0):
        super().__init__(cards, status)
        # Attributes
        self._wager = wager
        self._insurance = insurance
        self._handNumber = handNumber
        self._status = status
        
        # Metadata
        self.outcome = None
        self.earnings = 0
        self.lost_insurance = False

    # def pretty_format(self):
    #     """Get a string representation of the hand formatted to be printed."""
    #     # Display the case where a hand lost it's insurance side bet
    #     extra_outcome = ''
    #     if self.lost_insurance:
    #         extra_outcome += ' (Lost Insurance Bet)'
        
    #     lines = [
    #         f"Hand {self.hand_number}:",
    #         f"Cards: {self}",
    #         f"Total: {self.get_total_to_display()}",
    #         f"Wager: {_loggingController.GetMoneyFormat(self.wager)}",
    #         f"Status: {self.Status}",
    #         f"Outcome: {self.outcome}{extra_outcome}",
    #         f"Net: {_loggingController.GetMoneyFormat(self.earnings - self.wager - self.insurance)}"
    #     ]
        
    #     return '\n\t'.join(lines)


    def IsSplittable(self):
        """
        Check whether the hand is splittable. 
        Requirements:
        1) Hand is made up of two cards.
        2) The value of the two cards matches (e.g. King-King, Five-Five, etc.)
        """
        return len(self.Cards) == 2 and self.Cards[0].Rank == self.Cards[1].Rank


    def IsDoubleable(self):
        """
        Check whether the hand is doubleable. 
        Requirements:
        1) Hand is made up of two cards.
        """
        return len(self.Cards) == 2
    