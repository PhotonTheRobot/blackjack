from blackjack.display_utils import money_format
from blackjack.values import HandStatus
from blackjack.values.CardRanks import CardRank


class Hand:

    def __init__(self, cards=None, status=HandStatus.Waiting):
        self.cards = cards or []  # Card order matters for consistent display
        self.status = status

        if self.IsBlackjack():
            self.status = HandStatus.Blackjack

    def __str__(self):
        return ' | '.join(str(card) for card in self.cards)

    def __repr__(self):
        return self.__str__()

    def PossibleTotals(self):
        """Sum the cards in the hand. Return 2 totals, due to the dual value of Aces."""
        # Get the number of aces in the hand
        num_aces = self.get_num_aces_in_hand()

        # Get the total for all non-ace cards first, as this is constant
        non_ace_total = sum(card.value for card in self.cards if card.name != 'Ace')

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

    def GetTotalAces(self):
        """Get the number of Aces in the hand."""
        return sum(1 for card in self.cards if card.rank == CardRank.Ace)

    def format_possible_totals(self):
        """Get human readable string representing the hand total(s) to display."""
        # Get possible hand total(s) to display
        low_total, high_total = self.possible_totals()

        # Return string of total that makes sense
        if high_total == 21:
            return f"{high_total}"
        elif high_total:
            return f"{low_total} or {high_total}"
        else:
            return f"{low_total}"

    def FinalTotal(self):
        """Get the singular hand total for determining the outcome (high total if it exists, otherwise low total)."""
        low_total, high_total = self.possible_totals()
        return high_total or low_total

    def get_total_to_display(self):
        """Get the hand total to display contingent on hand status."""
        # If hand is still active, allow for multiple totals to be displayed. Otherwise, display the single final total.
        if self.status in (HandStatus.Waiting, HandStatus.Playing):
            return self.format_possible_totals()
        else:
            return str(self.final_total())

    def Is21(self):
        """Check if the hand totals to 21."""
        return self.final_total() == 21

    def IsBlackjack(self):
        """Check whether the hand is blackjack."""
        return self.is_21() and len(self.cards) == 2

    def IsBusted(self):
        """Check whether the hand is busted."""
        return self.final_total() > 21

    def IsSoft(self):
        """Check whether a hand is 'soft', meaning has an Ace counted as 11."""
        _, high_total = self.possible_totals()
        return bool(high_total)