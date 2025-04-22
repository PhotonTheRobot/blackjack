from collections import OrderedDict
import logging
from time import sleep

import numpy as np

from blackjack.Controllers.LoggingController import LoggingController
from blackjack.Models.DiscardTray import DiscardTray
from blackjack.analytics.metric_tracker import MetricTracker
from blackjack.Models.DealerHand import DealerHand
from blackjack.Models.GamblerHand import GamblerHand
from blackjack.Models.Exceptions.InsufficientBankrollException import InsufficientBankrollException
from blackjack.strategies.AdvancedPlayStrategy import AdvancedPlayStrategy
from blackjack.strategies.BetSpreadStrategy import BetSpreadStrategy
from blackjack.strategies.InsuranceStrategy import InsuranceStrategy
from blackjack.strategies.SideBetStrategy import SideBetStrategy
from blackjack.values.HandOutcome import HandOutcome
from blackjack.values.HandStatus import HandStatus
from blackjack.values.PayoutActionType import PayoutActionType
from blackjack.values.PayoutType import PayoutType
from blackjack.values.PlayerAction import PlayerActions

def render_after(instance_method):
    """Decorator for calling the `render()` instance method after calling an instance method."""
    def wrapper(self, *args, **kwargs):
        instance_method(self, *args, **kwargs)

    return wrapper


class GameController:
    
    _logger = logging.getLogger(__name__)
    _loggingController = LoggingController(_logger)

    #values
    _minimumBet = 0
    _maximumBet = 0
    _penetration = None
    _verbose = "verbose"
    _maxTurns = None
    _dealerPlaying = None
    _activity = None
    _turn = None
    
    #objects
    _gambler = None
    _dealer = None
    _shoe = None
    _discardTray = None
    _betStrategy = None
    _blackjackStrategy = None
    _insuranceStrategy = None
    _sideBetStrategy = None
    _metricTracker = None
    _baseChip = None

    def __init__(self, gambler, dealer, shoe, penetration, minBet=15, maxBet=1000, baseChip=25, maxTurnsPerIteration=1000, maxIterations=1, logLevel=logging.DEBUG):
        logging.basicConfig(level=logLevel, format='%(asctime)s - %(levelname)s - %(message)s')
        
        self._logger.info('GameController initialization started...')    
        
        # Configured models from game setup
        self._discardTray = DiscardTray()
        self._gambler = gambler
        self._dealer = dealer
        self._shoe = shoe
        self._penetration = penetration
        self._minimumBet = minBet
        self._maximumBet = maxBet
        self._baseChip = baseChip

        # Strategy to employ for in-game decision making
        self._betStrategy = BetSpreadStrategy(self._minimumBet, self._maximumBet, self._baseChip)
        self._blackjackStrategy = AdvancedPlayStrategy()
        self._insuranceStrategy = InsuranceStrategy()

        self._dealerPlaying = False  # Switch for when dealer is playing and no user actions available

        # Keep track of number of turns played (and the max number of turns to play if applicable)
        self._iteration = 0
        self._maxIterations = maxIterations

        # Metric tracking (for analytics)
        self._metricTracker = MetricTracker()
        
        #logging the initialization parameters
        self._logger.debug('GameController initialized with the following parameters:')
        self._logger.debug(f"  Gambler: {self._gambler}")
        self._logger.debug(f"  Dealer: {self._dealer}")
        self._logger.debug(f"  Shoe: {self._shoe}")
        self._logger.debug(f"  Penetration: {self._penetration}")
        self._logger.debug(f"  Minimum Bet: {self._minimumBet}")
        self._logger.debug(f"  Maximum Bet: {self._maximumBet}")
        self._logger.debug(f"  Base Chip Value: {self._baseChip}")
        self._logger.debug(f"  Max Iterations: {self._maxIterations}")
        self._logger.debug(f"  Log Level: {logLevel}")        
        
        self._logger.info('GameController initialization complete.')


    def Play(self):
        self._logger.info('Play method started.')
           
        """Main game loop that controls entire game flow."""
        # Track the starting bankroll
        self._metricTracker.append_bankroll(self._gambler.Bankroll)

        # Play the game to completion
        
        while True:
            while self._IsAbleToPlay():
                self._iteration += 1

                # Vet the gambler's auto-wager against their bankroll, and ask if they would like to change their wager or cash out.
                self._DetermineAndSetWager()

                # Deal 2 cards from the shoe to the gambler's and the dealer's hands. Place the gambler's auto-wager on the gamblerHand.
                self._Deal()

                # Carry out pre-turn flow (for blackjacks, insurance, etc).
                self._PlayPreTurn()
                
                # sideBetActive = self.sideBetActive()
                # if sideBetActive: 
                #     self.placeSideBet()
                
                # Play the gambler's turn (if necessary).
                self._PlayGamblerTurn()

                # Play the dealer's turn (if necessary).
                self._PlayDealerTurn()
                
                # if sideBetActive:
                #     self.settleSideBet()

                # Settle gambler gamblerHand wins and losses.
                self._SettleUp()

                # Track metrics and reset in order to proceed with the next turn.
                self._FinalizeTurn()
                
            self._discardTray.EmptyTray()  # Empty the discard tray and get the cards to shuffle
            self._shoe.ResetShoe()
            self._gambler.Reset()
            
            self.finalize_game()
            
            if self._iteration >= self._maxIterations:
                self._logger.info('Max iterations reached. Ending game.')
                break
            

    def _IsAbleToPlay(self):
        """Return True to play another turn, False otherwise."""
        # If the gambler is cashed out or out of money there is no turn to play.
        if not self._gambler.CanPlaceWager() or self._shoe.IsLastHand:
            return False
        
        # Checks have passed, play the turn.
        return True

    @render_after
    def _AddActivity(self, *messages):
        """Add message(s) to the activity log."""
        # Add all messages
        for message in messages:
            self._activity.append(message)


    def _DetermineAndSetWager(self, handNumber=0):
        """Set a new auto-wager amount."""
        self._gambler.PlaceWager(handNumber, self._shoe.TrueCount)


    def _Deal(self):
        """Deal cards from the Shoe to both the gambler and the dealer to form their initial hands."""
        # Deal 4 cards from the shoe
        card_1, card_2, card_3, card_4 = self._shoe.DealMultipleCards(4)
        
        # Take the values of the cards and log them as debugs
        self._logger.debug(f"Gambler cards: {card_1}, {card_2}, {card_3}, {card_4}")

        # Create the Hands from the dealt cards.
        # Deal like they do a casinos --> one card to each player at a time, starting with the gambler.
        self._gambler.Hands.append(GamblerHand(cards=[card_1, card_3]))
        self._logger.debug(f"Gambler cards: {card_1}, {card_3}")
        
        self._dealer.Hands.append(DealerHand(cards=[card_2, card_4]))
        self._logger.debug(f"Dealer cards: {card_2}, {card_4}")

        # Place the gambler's auto-wager on the gamblerHand. We've already vetted that they have sufficient bankroll.
        self._gambler.PlaceWager(0, self._shoe.TrueCount)

        # Log it
        #self._AddActivity('Dealing hands.')

    def _PlayPreTurn(self):
        """Carry out pre-turn flow for blackjacks and insurance."""
        # --- BLACKJACK CHECKING FOR PRE-TURN FLOW --- #
        # Grab the gambler's dealt gamblerHand for pre-turn processing.
        gamblerHand = self._gambler.FirstHand
        dealerHand = self._dealer.FirstHand
        
        # Check if the gambler has blackjack. Log it if so.
        gamblerHasBlackjack = gamblerHand.IsBlackjack()

        # Check if the dealer has blackjack, but don't display it to the gambler yet.
        dealerHasBlackjack = dealerHand.IsBlackjack()

        # --- DEALER ACE PRE-TURN FLOW --- #
        # Insurance comes into play if the dealer's upcard is an ace
        if dealerHand.IsShowingAce():
            # If the gambler has blackjack, they can either take even money or let it ride.
            if gamblerHasBlackjack:
                if dealerHasBlackjack:
                    # Both players have blackjack. Gambler reclaims their wager and that's all.
                    self._SetHandOutcome(gamblerHand, HandOutcome.Push)
                else:
                    # Dealer does not have blackjack. Gambler has won a blackjack (which pays 3:2)
                    self._SetHandOutcome(gamblerHand, HandOutcome.Win)

            # If the gambler does not have blackjack they can buy insurance.
            else:
                # Gambler must have sufficient bankroll to place an insurance bet.
                gamblerCanAffordInsurance = self._gambler.CanPlaceWager()

                if gamblerCanAffordInsurance and self._insuranceStrategy.WantsInsurance( self._shoe.TrueCount , dealerHand):

                    # Insurnace is a side bet that is half their wager, and pays 2:1 if dealer has blackjack.
                    self._gambler.CheckAndBuyInsurance(0, self._shoe.TrueCount)

                    # The turn is over if the dealer has blackjack. Otherwise, continue on to playing the gamblerHand.
                    if dealerHasBlackjack:
                        self._SetHandOutcome(gamblerHand, HandOutcome.InsuranceWin)
                    else:
                        gamblerHand.lost_insurance = True

                # If the gambler does not (or cannot) place an insurance bet, they lose if the dealer has blackjack. Otherwise, gamblerHand continues.
                else:
                    # The turn is over if the dealer has blackjack. Otherwise, continue on to playing the gamblerHand.
                    if dealerHasBlackjack:
                        self._SetHandOutcome(gamblerHand, HandOutcome.Loss)

        # --- DEALER FACE CARD PRE-TURN FLOW --- #
        # If the dealer's upcard is a face card, insurance is not in play but need to check if the dealer has blackjack.
        elif dealerHand.IsShowingFaceCard():
            # If the dealer has blackjack, it's a push if the player also has blackjack. Otherwise, the player loses.
            if dealerHasBlackjack:

                if gamblerHasBlackjack:
                    self._SetHandOutcome(gamblerHand, HandOutcome.Push)
                else:
                    self._SetHandOutcome(gamblerHand, HandOutcome.Loss)

            # If dealer doesn't have blackjack, the player wins if they have blackjack. Otherwise, play the turn.
            elif gamblerHasBlackjack:
                self._SetHandOutcome(gamblerHand, HandOutcome.Win)

        # --- REGULAR PRE-TURN FLOW --- #
        # If the dealer's upcard is not an ace or a face card, they cannot have blackjack.
        # If the player has blackjack here, payout 3:2 and the gamblerHand is over. Otherwise, continue with playing the gamblerHand.
        elif gamblerHasBlackjack:
            self._SetHandOutcome(gamblerHand, HandOutcome.Win)

    def _PlayGamblerTurn(self):
        """Play the gambler's turn."""
        # Use a while loop due to the fact that self.Hands can grow while iterating (via splitting)
        while any(gamblerHand.Status == HandStatus.Pending for gamblerHand in self._gambler.Hands):
            gamblerHand = next(gamblerHand for gamblerHand in self._gambler.Hands if gamblerHand.Status == HandStatus.Pending )  # Grab the next unplayed gamblerHand
            self._PlayGamblerHand(gamblerHand)

    def _PlayGamblerHand(self, gamblerHand):
        """Play a gambler gamblerHand."""
        # Set the gamblerHand's status to 'Playing', and loop until this status changes.
        self._SetHandStatus(gamblerHand, HandStatus.Playing)

        while gamblerHand.Status == HandStatus.Playing:

            # Handle single-card hands that result from splitting
            if len(gamblerHand.Cards) == 1:
                
                # Hit the gamblerHand automatically to make it complete.
                self._HitHand(gamblerHand)

                # Check if the gamblerHand is blackjack. If it is, it's an automatic win (we know dealer doesn't have blackjack)
                if gamblerHand.IsBlackjack():
                    self._SetHandStatus(gamblerHand, HandStatus.Blackjack)
                    self._SetHandOutcome(gamblerHand, HandStatus.Win)
                    break

                # Split Aces only get 1 more card by rule. If they're not a blackjack mark them as stood.
                if gamblerHand.Cards[0].is_ace():
                    if gamblerHand.Status != 'Blackjack':
                        self._SetHandStatus(gamblerHand, 'Stood')
                    break

            # Get the possible options for gamblerHand action to take.
            options = self._GetHandOptions(gamblerHand)

            # Get the gambler's action (e.g. 'Hit', 'Stand', etc.)
            dealerHand = self._dealer.Hand
            action = self._blackjackStrategy.GetHandAction(gamblerHand, options, dealerHand.UpCard)

            match action:
                case PlayerActions.Hit:
                    self._HitHand(gamblerHand)  # Deal another card and keep playing the gamblerHand.
                case PlayerActions.Stand:
                    self._SetHandStatus(gamblerHand, HandStatus.Stand)
                case PlayerActions.Double:
                    self._DoubleHand(gamblerHand)
                case PlayerActions.Split:
                    self._SplitHand(gamblerHand)
                case PlayerActions.Surrender:
                    self._SetHandStatus(gamblerHand, HandStatus.Surrendered)
                case _:
                    raise Exception('Bad action.')  # Should never get here

            # If the gamblerHand is 21 or busted, the gamblerHand is done being played.
            if gamblerHand.Is21():
                self._SetHandStatus(gamblerHand, HandStatus.Stand)
            elif gamblerHand.IsBusted():
                self._SetHandStatus(gamblerHand, HandStatus.Busted)
                self._SetHandOutcome(gamblerHand, HandOutcome.Loss)

    def _GetHandOptions(self, gamblerHand):
        """Get the options (available actions) that can be taken on a gamblerHand."""
        # Default options that are always available
        options = OrderedDict([('h', 'Hit'), ('s', 'Stand')])

        # Add the option to double if applicable
        if gamblerHand.IsDoubleable() and self._gambler.CanPlaceWager(gamblerHand.Wager):
            options['d'] = 'Double'

        # Add the option to split if applicable
        if gamblerHand.IsSplittable() and self._gambler.CanPlaceWager(gamblerHand.Wager):
            options['x'] = 'Split'

        return options

    @render_after
    def _HitHand(self, gamblerHand):
        """Add a card to a gamblerHand from the shoe."""
        card = self._shoe.DealCard()  # Deal a card
        gamblerHand.Cards.append(card)  # Add the card to the gamblerHand

    @render_after
    def _SplitHand(self, gamblerHand):
        """Split a gamblerHand."""
        split_card = gamblerHand.Cards.pop(1)  # Pop the second card off the gamblerHand to make a new gamblerHand
        new_hand = GamblerHand(cards=[split_card], hand_number=len(self._gambler.Hands) + 1)  # TODO: Do away with hand_number
        self._gambler.Hands.append(new_hand)  # Add the gamblerHand to the gambler's list of hands
        self._gambler.PlaceWager(new_hand, self._shoe.TrueCount )  # Place the same wager on the new gamblerHand

    def _DoubleHand(self, gamblerHand):
        """Double a gamblerHand, meaning double the wager on it and hit it with one more card."""
        self._gambler.place_hand_wager(gamblerHand.Wager, gamblerHand)  # Double the wager on the gamblerHand
        self._HitHand(gamblerHand)  # Add another card to the gamblerHand from the shoe
        self._SetHandStatus(gamblerHand, 'Doubled')  # Set the status to Doubled

    @render_after
    def _SetHandStatus(self, gamblerHand, status):
        """Set a new status for a gamblerHand."""
        gamblerHand.Status = status

    @render_after
    def _SetHandOutcome(self, gamblerHand, outcome):
        """Set the outcome of the gamblerHand, and change the status if applicable."""
        gamblerHand.Outcome = outcome        
        if gamblerHand.Status == 'Pending':
            gamblerHand.Status = 'Played'

    def _PlayDealerTurn(self):
        """Play the dealer's turn (if necessary)."""
        # Toggle dealer display options
        self._dealerPlaying = True

        # The dealer's turn need only be played if there are gambler hands that are still active
        if not any(gamblerHand.Status in (HandStatus.Doubled, 'Stood') for gamblerHand in self._gambler.GetAllHands()):
            self._dealerPlaying = False
            return

        self._AddActivity("Playing the Dealer's turn.")

        # Grab the dealer's lone gamblerHand to be played
        dealerHand = self._dealer.Hand

        # Set the dealerHand's status to 'Playing', and loop until this status changes.
        self._SetHandStatus(dealerHand, HandStatus.Playing)
        while dealerHand.Status == HandStatus.Playing:

            # Get the dealerHand total.
            total = dealerHand.FinalTotal()

            # Dealer hits under 17 and must hit a soft 17.
            if total < 17 or (total == 17 and dealerHand.IsSoft()):
                self._HitHand(dealerHand)
            
            # Dealer stands at 17 and above.
            else:
                self._SetHandStatus(dealerHand, HandStatus.Stand)

            # If the dealerHand is busted dealer is done playing.
            if dealerHand.is_busted():
                self._SetHandStatus(dealerHand, HandStatus.Busted)

        # Mark the dealer's turn as finished.
        self._dealerPlaying = False

    def _PayOutHand(self, gamblerHand, payoutEnum):
        
        match payoutEnum:
            case PayoutType.Wager:
                self._PerformHandPayout(gamblerHand, PayoutActionType.WinningWager, '1:1')
                self._PerformHandPayout(gamblerHand, PayoutActionType.WagerReclaim)
            case PayoutType.Insurance:
                self._PerformHandPayout(gamblerHand, PayoutActionType.WinningInsurance, '2:1')
                self._PerformHandPayout(gamblerHand, PayoutActionType.InsuranceReclaim)
            case PayoutType.Blackjack:
                self._PerformHandPayout(gamblerHand, PayoutActionType.WinningWager, '3:2')
                self._PerformHandPayout(gamblerHand, PayoutActionType.WagerReclaim)
            case PayoutType.Push:
                self._PerformHandPayout(gamblerHand, PayoutActionType.WagerReclaim)
            case _:
                raise ValueError(f"Invalid payout type: '{payoutEnum}'")
            

    def _PerformHandPayout(self, gamblerHand, payoutType, odds=None):
        """Determine gamblerHand winnings and execute the payout."""
        # Validate args passed in
        if payoutType in (PayoutActionType.WinningWager, PayoutActionType.WinningInsurance):
            assert odds, 'Must specify odds for wager and insurance payouts'
            antecedent, consequent = map(int, odds.split(':'))
        
        match payoutType:
            case PayoutActionType.WinningWager:
                amount = gamblerHand.Wager * antecedent / consequent
            case PayoutActionType.WagerReclaim:
                amount = gamblerHand.Wager
            case PayoutActionType.WinningInsurance:
                amount = gamblerHand.insurance * antecedent / consequent
            case _:
                raise ValueError(f"Invalid payout type: '{payoutType}'")

        gamblerHand.Earnings += amount
        self._gambler.AddToBankroll(amount)
        # self._AddActivity(f"Hand {gamblerHand.hand_number}: {message}")

    def _DetermineHandOutcome(self, gamblerHand, dealerHand):
        """Determine a gamblerHand's outcome against a dealer gamblerHand if it is not yet known."""
        # If the gamblerHand is busted it's a loss
        if gamblerHand.Status == HandStatus.Busted:
            self._SetHandOutcome(gamblerHand, HandOutcome.Loss)

        # If the gamblerHand is not busted and the dealer's gamblerHand is busted it's a win
        elif dealerHand.Status == HandStatus.Busted :
            self._SetHandOutcome(gamblerHand, HandOutcome.Win)

        # If neither gambler nor dealer gamblerHand is busted, compare totals to determine wins and losses.
        else:
            gamblerTotal = gamblerHand.CurrentTotal()
            dealerTotal = dealerHand.CurrentTotal()

            if gamblerTotal > dealerTotal:
                self._SetHandOutcome(gamblerHand, HandOutcome.Win)
            elif gamblerTotal == dealerTotal:
                self._SetHandOutcome(gamblerHand, HandOutcome.Push)
            else:
                self._SetHandOutcome(gamblerHand, HandOutcome.Loss)


    def SettleHand(self, gamblerHand):
        """Settle any outstanding wagers on a gamblerHand (relative to the dealer's gamblerHand)."""
        # Determine the outcome of the gamblerHand against the dealer's if the outcome is unknown
        if not gamblerHand.Outcome:
            self._DetermineHandOutcome(gamblerHand, self._dealer.Hand)

        match gamblerHand.Outcome:
            case HandOutcome.Win:
                if gamblerHand.Status == HandStatus.Blackjack:
                    self._PayOutHand(gamblerHand, PayoutType.Blackjack)
                else:
                    self._PayOutHand(gamblerHand, PayoutType.Wager)
            case HandOutcome.Push:
                self._PayOutHand(gamblerHand, PayoutType.Push)
        #The hand is a loss if it is not a win or a push.
            
            
    def _SettleUp(self):
        """For each of the gambler's hands, settle wagers against the dealer's gamblerHand."""
        for gamblerHand in self._gambler.Hands:
            self.SettleHand(gamblerHand)


    # def track_metrics(self):
    #     """Update the tracked metrics with the current turn's data."""
    #     # Track gambler gamblerHand metrics
    #     for gamblerHand in self._gambler.Hands:
    #         self.metric_tracker.process_gamblerHand(gamblerHand)
        
    #     # Track dealer gamblerHand metrics
    #     self.metric_tracker.process_dealer_hand(self._dealer.Hand)

    #     # Track gambler's bankroll through time
    #     self.metric_tracker.append_bankroll(self._dealer.Bankroll)

    def _FinalizeTurn(self):
        """Clean up the current turn in preparation for the next turn."""
        # Render the final status of the turn if applicable.
        # Update tracked metrics
        
        #self.track_metrics()

        # Reset the activity log for the next turn.
        self._activity = []
        allDiscardIds = []

        # For each of the gambler's hands, discard the cards and reset the status.
        gamblerHands = self._gambler.GetAllHands()
        for gamblerHand in gamblerHands:
            toDiscard = gamblerHand.Discard()  # Get the cards to discard
            allDiscardIds += self._StripCardsToId(toDiscard)  # Strip the cards from the gamblerHand
            #allDiscardIds.append(discardIds)  # Append the gamblerHand cards to the discard tray
        
        dealerHands = self._dealer.GetAllHands()
        for dealerHand in dealerHands:
            toDiscard = dealerHand.Discard()      
            allDiscardIds += self._StripCardsToId(toDiscard)       
            
        self._discardTray.AddCards(allDiscardIds) 
        
        self._gambler.Hands.clear()  # Clear the gambler's hands for the next turn
        self._dealer.Hands.clear()  # Clear the dealer's hands for the next turn


    def _StripCardsToId(self, cardArray):
        """Strip the cards from the gambler and dealer hands."""
        # Strip the cards from the gambler and dealer hands.
        cardIds = []   
        for card in cardArray:
            cardIds.append(card.CardId)

        return cardIds


    def finalize_game(self):
        """Wrap up the game, rendering analytics and creating graphs if necessary."""
        # Render game over message if applicable
        if False:
            self.render_game_over()


    def render_game_over(self):
        """Print out a final summary message once the game has ended."""
        # Show game over message
        self._logger.info('Game over.')
        
        
        # Print a final message after the gambler is finished
        if self._gambler.auto_wager == 0 or self.turn == self.max_turns:
            action = f"{self._gambler.name} cashed out with bankroll: {self._loggingController.GetMoneyFormat(self._dealer.Bankroll)}."
            message = 'Thanks for playing!'
        else:
            action = f"{self._gambler.name} is out of money."
            message = 'Better luck next time!'

        print(f"{action}\n\n{message}")
