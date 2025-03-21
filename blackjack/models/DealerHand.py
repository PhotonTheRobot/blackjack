from blackjack.display_utils import money_format
from blackjack.values.CardRanks import CardRank

class DealerHand(Hand):

    def UpCard(self):
        return self.cards[0]

    # def pretty_format(self, hide=True):
    #     """Get a string representation of the hand formatted to be printed."""
    #     if hide:
    #         up_card = self.up_card()
    #         cards = f"Upcard: {up_card}"
    #         total = f"Total: {up_card.value if up_card.name != 'Ace' else '1 or 11'}"
    #         status = 'Status: Pending'
    #     else:
    #         cards = f"Cards: {self}"
    #         total = f"Total: {self.get_total_to_display()}"
    #         status = f"Status: {self.status}"

    #     lines = [
    #         'Hand:',
    #         cards,
    #         total,
    #         status
    #     ]
    #     return '\n\t'.join(lines)
