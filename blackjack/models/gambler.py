from blackjack.exc import InsufficientBankrollError, OverdraftError
from blackjack.display_utils import money_format


class Gambler:
    _bankroll = 0
    _isRuined = False
    _hands = []
    _defaultWager = 0


    def __init__(self, bankroll=0, hands=[]):
        self._bankroll = bankroll
        self._hands = hands
        

    # def __str__(self):
    #     return f"Player: {self.name} | Bankroll: {money_format(self.bankroll)}"

    def EmptyHands(self):
        """Empty the hand."""
        self.hands = []


    def GetHand(self, handNumber):
        """Helper method for action that happens on the initial hand dealt to the gambler."""
        return self.hands[handNumber]
    
    
    def CanPlaceWager(self, wager):
        """Check if a wager can be placed."""
        return wager <= self.bankroll


    def AddToBankroll(self, amount):
        """Add an amount to the bankroll."""
        self.bankroll += amount


    def RemoveFromBankroll(self, amount):
        if self.CanPlaceWager():
            self.bankroll -= amount
        else:
            raise InsufficientBankrollError('Insufficient bankroll to place wager')

    def PlaceWager(self, wager, handNumber):
        """Place a wager on a hand. Additive so can be used to double down."""
        self._subtract_bankroll(wager)  
        if self.bankroll <= 0:
            raise OverdraftError('The player\'s bankroll has been ruined')
        
        self.Hands[handNumber].wager = wager
        

    def BuyInsurance(self, handNumber):
        hand = self.hands[handNumber]
        insuranceAmount = hand.wager / 2
        
        if self.CanPlaceWager(insuranceAmount):
            self.RemoveFromBankroll(insuranceAmount)
            hand.insurance = insuranceAmount
        else:
            raise InsufficientBankrollError('Insufficient bankroll to place insurance bet')


    def SettleUp(self, dealer_hand):
        """Compare Gambler hands to a given Dealer hand."""
        for hand in self.hands:
            hand.settle_up(dealer_hand)


    def DoubleDown(self, handNumber):
        """Double down on a hand."""
        hand = self.hands[handNumber]
        wager = hand.wager
        self.PlaceWager(wager, handNumber)
        hand.double_down = True
    
    
    def SplitHand(self, handNumber):
        """Split a hand."""
        hand = self.hands[handNumber]
        wager = hand.wager
        self.PlaceWager(wager, handNumber)
        new_hand = Hand([hand.cards.pop()])
        new_hand.wager = wager
        self.hands.append(new_hand)