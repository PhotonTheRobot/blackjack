from blackjack.models.Hand import Hand
from blackjack.models.Participant import Participant
from blackjack.models.exceptions.InsufficientBankrollException import InsufficientBankrollException
from blackjack.models.exceptions.OverdraftException import OverdraftException


class Gambler(Participant):
    _bankroll = 0
    _isRuined = False
    _defaultWager = 0
    _autoWager = 0

    def __init__(self, bankroll=0, hands=[]):
        Participant.__init__(self, hands)
        self._bankroll = bankroll
        
        
    def CanPlaceWager(self, wager=0):
        if wager == 0:
            wager = self._defaultWager
            
        """Check if a wager can be placed."""
        return wager <= self._bankroll


    def GetBankroll(self):
        """Add an amount to the bankroll."""
        return self._bankroll
        

    def AddToBankroll(self, amount):
        """Add an amount to the bankroll."""
        self._bankroll += amount


    def RemoveFromBankroll(self, amount):
        if self.CanPlaceWager():
            self._bankroll -= amount
        else:
            raise InsufficientBankrollException('Insufficient bankroll to place wager')

    def SetAutoWager(self, wager = 0):
        """Get the wager based off of shoe's running count"""
        if wager == 0:
            wager = self._defaultWager
        
        self._wager = wager

    def PlaceWager(self, handNumber):
        """Place a wager on a hand. Additive so can be used to double down."""
        self._subtract_bankroll(self._autoWager)  
        if self._bankroll <= 0:
            raise OverdraftException('The player\'s bankroll has been ruined')
        
        self._hands[handNumber].Wager = self._autoWager
        

    def BuyInsurance(self, handNumber):
        hand = self._hands[handNumber]
        insuranceAmount = hand.wager / 2
        
        if self.CanPlaceWager(insuranceAmount):
            self.RemoveFromBankroll(insuranceAmount)
            hand.insurance = insuranceAmount
        else:
            raise InsufficientBankrollException('Insufficient bankroll to place insurance bet')


    def SettleUp(self, dealer_hand):
        """Compare Gambler hands to a given Dealer hand."""
        for hand in self._hands:
            hand.SettleUp(dealer_hand)


    def DoubleDown(self, handNumber):
        """Double down on a hand."""
        hand = self._hands[handNumber]
        wager = hand.wager
        self.PlaceWager(wager, handNumber)
        hand.double_down = True
    
    
    def SplitHand(self, handNumber):
        """Split a hand."""
        hand = self._hands[handNumber]
        wager = hand.wager
        self.PlaceWager(wager, handNumber)
        new_hand = Hand([hand.cards.pop()])
        new_hand.wager = wager
        self._hands.append(new_hand)