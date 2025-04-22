

from blackjack.Models.Exceptions.InsufficientBankrollException import InsufficientBankrollException
from blackjack.values.CardRank import CardRank
from blackjack.values.HandStatus import HandStatus

#Hand class
class Hand:
    _cards = []
    _status = HandStatus.Pending
    _insurance = 0
    _wager = 0
    
    @property
    def Wager(self):
        """Get the wager on the hand."""
        return self._wager
    
    @property
    def Cards(self):
        """Get the cards in the hand."""
        return self._cards
    
    @property
    def Status(self):
        """Get the status of the hand."""
        return self._status
    @Status.setter
    def Status(self, status):
        """Set the status of the hand."""
        self._status = status

    #Constructor
    def __init__(self, cards=[], status=HandStatus.Pending):
        self._cards = cards
        self._status = status

        if self.IsBlackjack():
            self._status = HandStatus.Blackjack

    def __str__(self):
        return ' | '.join(str(card) for card in self._cards)

    def __repr__(self):
        return self.__str__()

    def _PossibleTotals(self):
        """Sum the cards in the hand. Return 2 totals, due to the dual value of Aces."""
        # Get the number of aces in the hand
        num_aces = self._GetTotalAces()

        # Get the total for all non-ace cards first, as this is constant
        non_ace_total = sum(card.CountValue for card in self._cards if card.Rank != CardRank.Ace)

        # If there are no aces in the hand, there is only one possible total. Return it.
        if num_aces == 0:
            return non_ace_total, None

        # If there are aces in the hand, extra logic is needed:
        # - Each ace can have 2 possible values (1 or 11). 
        # - However, only one ace *per hand* can logically be 11 in order to *possibly* stay under a total of 22.
        # - Thus, there will always be 2 *possibly non-busting* hand totals if there is at least one ace in the hand.
        high_total = non_ace_total + 11 + num_aces - 1
        low_total = non_ace_total + num_aces

        # If the high_total is already busting, only return the low_total (to be vetted for busting later)
        if high_total > 21:
            return low_total, None
        # Otherwise, return both totals
        else:
            return low_total, high_total

    def _GetTotalAces(self):
        """Get the number of Aces in the hand."""
        totalAces = sum(1 for card in self._cards if card.Rank == CardRank.Ace)
        return totalAces

    def _FormatPossibleTotals(self):
        """Get human readable string representing the hand total(s) to display."""
        # Get possible hand total(s) to display
        low_total, high_total = self._PossibleTotals()

        # Return string of total that makes sense
        if high_total == 21:
            return f"{high_total}"
        elif high_total:
            return f"{low_total} or {high_total}"
        else:
            return f"{low_total}"

    def CurrentTotal(self):
        """Get the singular hand total for determining the outcome (high total if it exists, otherwise low total)."""
        low_total, high_total = self._PossibleTotals()
        return high_total or low_total

    def _DisplayTotal(self):
        """Get the hand total to display contingent on hand status."""
        # If hand is still active, allow for multiple totals to be displayed. Otherwise, display the single final total.
        if self._status in (HandStatus.Waiting, HandStatus.Playing):
            return self.format__PossibleTotals()
        else:
            return str(self.CurrentTotal())

    def Is21(self):
        """Check if the hand totals to 21."""
        return self.CurrentTotal() == 21

    def IsBlackjack(self):
        """Check whether the hand is Blackjack."""
        return self.Is21() and len(self._cards) == 2

    def IsBusted(self):
        """Check whether the hand is busted."""
        return self.CurrentTotal() > 21

    def IsSoft(self):
        """Check whether a hand is 'soft', meaning has an Ace counted as 11."""
        _, high_total = self._PossibleTotals()
        return bool(high_total)
    
    def SetWager(self, wager=0):
        """Set the wager on the hand."""
        if wager == 0:
            wager = self._defaultWager
        self._wager = wager
        
    def Discard(self):
        """Empty the hand."""
        cardsToDiscard = self._cards
        
        for card in self._cards:
            self._cards = []
        
        self._status = HandStatus.Pending
        return cardsToDiscard