from blackjack.display_utils import money_format
from blackjack.models.hand import Hand
from blackjack.values import HandStatus
from blackjack.values.CardRanks import CardRank

class GamblerHand(Hand):

    def __init__(self, cards=None, status=HandStatus.Waiting, wager=0, insurance=0, hand_number=0):
        super().__init__(cards, status)
        # Attributes
        self.wager = wager
        self.insurance = insurance
        self.hand_number = hand_number
        
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
    #         f"Wager: {money_format(self.wager)}",
    #         f"Status: {self.status}",
    #         f"Outcome: {self.outcome}{extra_outcome}",
    #         f"Net: {money_format(self.earnings - self.wager - self.insurance)}"
    #     ]
        
    #     return '\n\t'.join(lines)

    def IsSplittable(self):
        """
        Check whether the hand is splittable. 
        Requirements:
        1) Hand is made up of two cards.
        2) The value of the two cards matches (e.g. King-King, Five-Five, etc.)
        """
        return len(self.cards) == 2 and self.cards[0].Rank == self.cards[1].Rank


    def IsDoubleable(self):
        """
        Check whether the hand is doubleable. 
        Requirements:
        1) Hand is made up of two cards.
        """
        return len(self.cards) == 2