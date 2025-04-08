from blackjack.Models.Hand import Hand
from blackjack.Models.Participant import Participant
from blackjack.Models.Exceptions.InsufficientBankrollException import InsufficientBankrollException
from blackjack.Models.Exceptions.OverdraftException import OverdraftException


class Gambler(Participant):
    _bankroll = 0
    _isRuined = False
    _minBet = 0
    _currentTrueCountWager = 0
    
    @property
    def Bankroll(self):
        """Get the bankroll."""
        return self._bankroll
    

    def __init__(self, gamblerConfig, minBet, hands=[]):
        Participant.__init__(self, hands)
        self._bankroll = gamblerConfig['bankroll']
        self._trueCountChipMultiplier = gamblerConfig['trueCountChipMultiplier']
        self._minBet = minBet
        self._currentTrueCountWager = minBet

        
    def CanPlaceWager(self, wager=0):
        if wager == 0:
            wager = self._minBet
            
        """Check if a wager can be placed."""
        return wager <= self._bankroll
        

    def AddToBankroll(self, amount):
        """Add an amount to the bankroll."""
        self._bankroll += amount


    def RemoveFromBankroll(self, amount):
        if self.CanPlaceWager():
            self._bankroll -= amount
        else:
            raise InsufficientBankrollException('Insufficient bankroll to place wager')


    def PlaceWager(self, handNumber = 0, trueCount = 0):
        """Place a wager on a hand. Additive so can be used to double down."""
        #assume the wager is the minimum bet unless otherwise specified
        self._currentTrueCountWager = self._minBet
        
        #if the true count is greater than 0, then the wager is the true count times the true count chip multiplier
        if trueCount > 0:
            self._currentTrueCountWager = trueCount * self._trueCountChipMultiplier
        
        self._bankroll -= self._currentTrueCountWager
        if self._bankroll <= 0:
            raise OverdraftException('The player\'s bankroll has been ruined')
        
        if len(self._hands) > 0:
            self.Hands[handNumber].SetWager( self._currentTrueCountWager )
        

    def CheckAndBuyInsurance(self, handNumber, trueCount = 0):
        hand = self._hands[handNumber]
        insuranceAmount = hand.Wager / 2
        
        if trueCount > 0:        
            if self.CanPlaceWager(insuranceAmount):
                self.RemoveFromBankroll(insuranceAmount)
                hand.Insurance = insuranceAmount
            else:
                raise InsufficientBankrollException('Insufficient bankroll to place insurance bet')


    def SettleUp(self, dealer_hand):
        """Compare Gambler hands to a given Dealer hand."""
        for hand in self._hands:
            hand.SettleUp(dealer_hand)


    def DoubleDown(self, handNumber):
        """Double down on a hand."""
        hand = self._hands[handNumber]
        wager = hand.Wager
        self.PlaceWager(wager, handNumber)
        hand.double_down = True
    
    
    def SplitHand(self, handNumber):
        """Split a hand."""
        hand = self._hands[handNumber]
        wager = hand.Wager
        self.PlaceWager(wager, handNumber)
        
        new_hand = Hand([hand.Cards.pop()])
        new_hand.SetWager(wager)
        self._hands.append(new_hand)