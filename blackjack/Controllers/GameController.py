from collections import OrderedDict
import logging
from time import sleep

from blackjack.analytics.metric_tracker import MetricTracker
from blackjack.Utilities.DisplayUtilities import clear, header, money_format, pct_format
from blackjack.Models.DealerHand import DealerHand
from blackjack.Models.GamblerHand import GamblerHand
from blackjack.Models.Exceptions.InsufficientBankrollException import InsufficientBankrollException
from blackjack.strategies.AdvancedPlayStrategy import AdvancedPlayStrategy
from blackjack.strategies.BetSpreadStrategy import BetSpreadStrategy
from blackjack.strategies.SideBetStrategy import SideBetStrategy
from blackjack.values.HandOutcome import HandOutcome
from blackjack.values.HandStatus import HandStatus




def render_after(instance_method):
    """Decorator for calling the `render()` instance method after calling an instance method."""
    def wrapper(self, *args, **kwargs):
        instance_method(self, *args, **kwargs)
        if self._verbose:
            self.render()
    return wrapper


class GameController:
    
    _logger = logging.getLogger(__name__)
    
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
    _strategy = None
    _metricTracker = None
    _baseChip = None

    def __init__(self, gambler, dealer, shoe, penetration, minBet=15, maxBet=1000, baseChip=25, maxTurnsPerIteration=1000, maxIterations=100, logLevel=logging.DEBUG):
        logging.basicConfig(level=logLevel, format='%(asctime)s - %(levelname)s - %(message)s')
        
        self._logger.info('GameController initialization started...')    
        
        # Configured models from game setup
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
        
        self._dealerPlaying = False  # Switch for when dealer is playing and no user actions available

        # Keep track of number of turns played (and the max number of turns to play if applicable)
        self._turn = 0
        self._maxTurns = maxTurnsPerIteration
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
        self._logger.debug(f"  Max Turns Per Iteration: {self._maxTurns}")
        self._logger.debug(f"  Max Iterations: {self._maxIterations}")
        self._logger.debug(f"  Log Level: {logLevel}")        
        
        self._logger.info('GameController initialization complete.')


    def Play(self):
        self._logger.info('Play method started.')
           
        """Main game loop that controls entire game flow."""
        # Track the starting bankroll
        self._metricTracker.append_bankroll(self._gambler.Bankroll)

        # Play the game to completion
        while self._IsAbleToPlay():
            self._turn += 1

            # Vet the gambler's auto-wager against their bankroll, and ask if they would like to change their wager or cash out.
            self._DetermineAndSetWager()

            # Deal 2 cards from the shoe to the gambler's and the dealer's hands. Place the gambler's auto-wager on the hand.
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

            # Settle gambler hand wins and losses.
            self._SettleUp()

            # Track metrics and reset in order to proceed with the next turn.
            self._FinalizeTurn()

        # Render a game over message
        self.finalize_game()

    def _IsAbleToPlay(self):
        """Return True to play another turn, False otherwise."""
        # If the gambler is cashed out or out of money there is no turn to play.
        if not self._gambler.CanPlaceWager():
            return False
        
        # If max number of turns imposed make sure we haven't hit it yet.
        if self._maxTurns:
            return self._turn < self._maxTurns
        
        # If the shoe has been penetrated, shuffle it and reset the penetration.
        if self._shoe.IsLastHand:
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
        # Set the gambler's auto_wager to $0.00.
        newWager = self._betStrategy.GetBidValue(self._shoe)
        self._gambler.PlaceWager(handNumber, newWager)
        
        self._logger.debug(f"New wager set to {money_format(newWager)}.")


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
        
        self._dealer.Hand.append(DealerHand(cards=[card_2, card_4]))
        self._logger.debug(f"Dealer cards: {card_2}, {card_4}")

        # Place the gambler's auto-wager on the hand. We've already vetted that they have sufficient bankroll.
        self._gambler.PlaceWager(0, self._shoe.TrueCount)

        # Log it
        #self._AddActivity('Dealing hands.')

    def _PlayPreTurn(self):
        """Carry out pre-turn flow for blackjacks and insurance."""
        # --- BLACKJACK CHECKING FOR PRE-TURN FLOW --- #
        # Grab the gambler's dealt hand for pre-turn processing.
        gamblerHand = self._gambler.FirstHand
        
        # Check if the gambler has blackjack. Log it if so.
        gamblerHasBlackJack = gamblerHand.IsBlackJack()

        # Check if the dealer has blackjack, but don't display it to the gambler yet.
        dealer_has_blackjack = self._dealer.PrimaryHand.IsBlackJack()

        # --- DEALER ACE PRE-TURN FLOW --- #
        # Insurance comes into play if the dealer's upcard is an ace
        if self._dealer.is_showing_ace():
            # If the gambler has blackjack, they can either take even money or let it ride.
            if gamblerHasBlackJack:
                if dealer_has_blackjack:
                    # Both players have blackjack. Gambler reclaims their wager and that's all.
                    self._SetHandOutcome(gamblerHand, HandOutcome.Push)
                else:
                    # Dealer does not have blackjack. Gambler has won a blackjack (which pays 3:2)
                    self._SetHandOutcome(gamblerHand, HandOutcome.Win)

            # If the gambler does not have blackjack they can buy insurance.
            else:
                # Gambler must have sufficient bankroll to place an insurance bet.
                gambler_can_afford_insurance = self._gambler.can_place_insurance_wager()

                if gambler_can_afford_insurance and self._strategy.wants_insurance():

                    # Insurnace is a side bet that is half their wager, and pays 2:1 if dealer has blackjack.
                    self._gambler.place_insurance_wager()

                    # The turn is over if the dealer has blackjack. Otherwise, continue on to playing the hand.
                    if dealer_has_blackjack:
                        self.hide_dealer = False  # Show the dealer's blackjack.
                        self._SetHandOutcome(gamblerHand, HandOutcome.InsuranceWin)
                    else:
                        gamblerHand.lost_insurance = True

                # If the gambler does not (or cannot) place an insurance bet, they lose if the dealer has blackjack. Otherwise, hand continues.
                else:
                    # The turn is over if the dealer has blackjack. Otherwise, continue on to playing the hand.
                    if dealer_has_blackjack:
                        self.hide_dealer = False
                        self._SetHandOutcome(gamblerHand, HandOutcome.Loss)

        # --- DEALER FACE CARD PRE-TURN FLOW --- #
        # If the dealer's upcard is a face card, insurance is not in play but need to check if the dealer has blackjack.
        elif self._dealer.is_showing_face_card():
            # If the dealer has blackjack, it's a push if the player also has blackjack. Otherwise, the player loses.
            if dealer_has_blackjack:

                self.hide_dealer = False
                
                if gamblerHasBlackJack:
                    self._SetHandOutcome(gamblerHand, HandOutcome.Push)
                else:
                    self._SetHandOutcome(gamblerHand, HandOutcome.Loss)

            # If dealer doesn't have blackjack, the player wins if they have blackjack. Otherwise, play the turn.
            elif gamblerHasBlackJack:
                self._SetHandOutcome(gamblerHand, HandOutcome.Win)

        # --- REGULAR PRE-TURN FLOW --- #
        # If the dealer's upcard is not an ace or a face card, they cannot have blackjack.
        # If the player has blackjack here, payout 3:2 and the hand is over. Otherwise, continue with playing the hand.
        elif gamblerHasBlackJack:
            self._SetHandOutcome(gamblerHand, HandOutcome.Win)

    def _PlayGamblerTurn(self):
        """Play the gambler's turn."""
        # Use a while loop due to the fact that self.hands can grow while iterating (via splitting)
        while any(hand.status == HandStatus.Pending for hand in self._gambler.hands):
            hand = next(hand for hand in self._gambler.hands if hand.status == HandStatus.Pending )  # Grab the next unplayed hand
            self._PlayGamblerHand(hand)

    def _PlayGamblerHand(self, hand):
        """Play a gambler hand."""
        # Set the hand's status to 'Playing', and loop until this status changes.
        self._SetHandStatus(hand, HandStatus.Playing)

        while hand.status == HandStatus.Playing:

            # Handle single-card hands that result from splitting
            if len(hand.cards) == 1:
                
                # Hit the hand automatically to make it complete.
                self._HitHand(hand)

                # Check if the hand is blackjack. If it is, it's an automatic win (we know dealer doesn't have blackjack)
                if hand.IsBlackJack():
                    self._SetHandStatus(hand, HandStatus.Blackjack)
                    self._SetHandOutcome(hand, HandStatus.Win)
                    break

                # Split Aces only get 1 more card by rule. If they're not a blackjack mark them as stood.
                if hand.cards[0].is_ace():
                    if hand.status != 'Blackjack':
                        self._SetHandStatus(hand, 'Stood')
                    break

            # Get the possible options for hand action to take.
            options = self._GetHandOptions(hand)

            # Get the gambler's action (e.g. 'Hit', 'Stand', etc.)
            action = self._strategy.get_hand_action(hand, options, self._dealer.up_card())

            if action == 'Hit':
                self._HitHand(hand)  # Deal another card and keep playing the hand.

            elif action == 'Stand':
                self._SetHandStatus(hand, 'Stood')  # Do nothing, hand is played.

            elif action == 'Double':
                self._DouleHand(hand)  # Double the wager and deal another card. Hand is played.

            elif action == 'Split':
                self._SplitHand(hand)  # Put the second card into a new hand and keep playing this hand.

            else:
                raise Exception('Unhandled response.')  # Should never get here

            # If the hand is 21 or busted, the hand is done being played.
            if hand.is_21():
                self._SetHandStatus(hand, 'Stood')
            elif hand.is_busted():
                self._SetHandStatus(hand, 'Busted')
                self._SetHandOutcome(hand, HandOutcome.Loss)

    def _GetHandOptions(self, hand):
        """Get the options (available actions) that can be taken on a hand."""
        # Default options that are always available
        options = OrderedDict([('h', 'Hit'), ('s', 'Stand')])

        # Add the option to double if applicable
        if hand.is_doubleable() and self._gambler.can_place_wager(hand.wager):
            options['d'] = 'Double'

        # Add the option to split if applicable
        if hand.is_splittable() and self._gambler.can_place_wager(hand.wager):
            options['x'] = 'Split'

        return options

    @render_after
    def _HitHand(self, hand):
        """Add a card to a hand from the shoe."""
        card = self.shoe.deal_card()  # Deal a card
        hand.cards.append(card)  # Add the card to the hand

    @render_after
    def _SplitHand(self, hand):
        """Split a hand."""
        split_card = hand.cards.pop(1)  # Pop the second card off the hand to make a new hand
        new_hand = GamblerHand(cards=[split_card], hand_number=len(self._gambler.hands) + 1)  # TODO: Do away with hand_number
        self._gambler.place_hand_wager(hand.wager, new_hand)  # Place the same wager on the new hand
        self._gambler.hands.append(new_hand)  # Add the hand to the gambler's list of hands

    def _DouleHand(self, hand):
        """Double a hand, meaning double the wager on it and hit it with one more card."""
        self._gambler.place_hand_wager(hand.wager, hand)  # Double the wager on the hand
        self._HitHand(hand)  # Add another card to the hand from the shoe
        self._SetHandStatus(hand, 'Doubled')  # Set the status to Doubled

    @render_after
    def _SetHandStatus(self, hand, status):
        """Set a new status for a hand."""
        hand.status = status

    @render_after
    def _SetHandOutcome(self, hand, outcome):
        """Set the outcome of the hand, and change the status if applicable."""
        hand.outcome = outcome        
        if hand.status == 'Pending':
            hand.status = 'Played'

    def _PlayDealerTurn(self):
        """Play the dealer's turn (if necessary)."""
        # Toggle dealer display options
        self.hide_dealer = False
        self._dealerPlaying = True

        # The dealer's turn need only be played if there are gambler hands that are still active
        if not any(hand.status in ('Doubled', 'Stood') for hand in self._gambler.GetAllHands()):
            self._dealerPlaying = False
            return

        self._AddActivity("Playing the Dealer's turn.")

        # Grab the dealer's lone hand to be played
        hand = self._dealer.Hand

        # Set the hand's status to 'Playing', and loop until this status changes.
        self._SetHandStatus(hand, 'Playing')
        
        while hand.status == 'Playing':

            # Pause for user to follow along if applicable
            if self.verbose:
                sleep(1)

            # Get the hand total.
            total = hand.final_total()

            # Dealer hits under 17 and must hit a soft 17.
            if total < 17 or (total == 17 and hand.is_soft()):
                self._HitHand(hand)
            
            # Dealer stands at 17 and above.
            else:
                self._SetHandStatus(hand, 'Stood')

            # If the hand is busted dealer is done playing.
            if hand.is_busted():
                self._SetHandStatus(hand, 'Busted')

        # Mark the dealer's turn as finished.
        self._dealerPlaying = False

    def _PayOutHand(self, hand, payout_type):
        """Pay out hand winnings, including wager reclaim."""
        # Pay out winning hand wagers 1:1 and reclaim the wager
        if payout_type == 'wager':
            self.perform_hand_payout(hand, 'winning_wager', '1:1')
            self.perform_hand_payout(hand, 'wager_reclaim')
        
        # Pay out winning blackjack hands 3:2 and reclaim the wager
        elif payout_type == 'blackjack':
            self.perform_hand_payout(hand, 'winning_wager', '3:2')
            self.perform_hand_payout(hand, 'wager_reclaim')

        # Pay out winning insurance wagers 2:1 and reclaim the insurance wager
        elif payout_type == 'insurance':
            self.perform_hand_payout(hand, 'winning_insurance', '2:1')
            self.perform_hand_payout(hand, 'insurance_reclaim')
        
        # Reclaim wager in case of a push
        elif payout_type == HandOutcome.Push:
            self.perform_hand_payout(hand, 'wager_reclaim')
        
        # Should not get here
        else:
            raise ValueError(f"Invalid payout type: '{payout_type}'")

    def perform_hand_payout(self, hand, payout_type, odds=None):
        """Determine hand winnings and execute the payout."""
        # Validate args passed in
        if payout_type in ('winning_wager', 'winning_insurance'):
            assert odds, 'Must specify odds for wager and insurance payouts!'
            antecedent, consequent = map(int, odds.split(':'))
        
        # Determine the payout amount by the payout_type (and odds if applicable)
        if payout_type == 'winning_wager':
            amount = hand.wager * antecedent / consequent
            message = f"Adding winning hand payout of {money_format(amount)} to bankroll."
        
        elif payout_type == 'wager_reclaim':
            amount = hand.wager
            message = f"Reclaiming hand wager of {money_format(amount)}."
        
        elif payout_type == 'winning_insurance':
            amount = hand.insurance * antecedent / consequent
            message = f"Adding winning insurance payout of {money_format(amount)} to bankroll."
        
        elif payout_type == 'insurance_reclaim':
            amount = hand.insurance
            message = f"Reclaiming insurance wager of {money_format(amount)}."

        else:
            raise ValueError(f"Invalid payout type: '{payout_type}'")

        hand.earnings += amount
        self._gambler.payout(amount)
        self._AddActivity(f"Hand {hand.hand_number}: {message}")

    def determine_hand_outcome(self, hand, dealer_hand):
        """Determine a hand's outcome against a dealer hand if it is not yet known."""
        # If the hand is busted it's a loss
        if hand.status == 'Busted':
            self._SetHandOutcome(hand, HandOutcome.Loss)

        # If the hand is not busted and the dealer's hand is busted it's a win
        elif dealer_hand.status == 'Busted':
            self._SetHandOutcome(hand, HandOutcome.Win)

        # If neither gambler nor dealer hand is busted, compare totals to determine wins and losses.
        else:
            hand_total = hand.final_total()
            dealer_hand_total = dealer_hand.final_total()

            if hand_total > dealer_hand_total:
                self._SetHandOutcome(hand, HandOutcome.Win)
            elif hand_total == dealer_hand_total:
                self._SetHandOutcome(hand, HandOutcome.Push)
            else:
                self._SetHandOutcome(hand, HandOutcome.Loss)

    def settle_hand(self, hand):
        """Settle any outstanding wagers on a hand (relative to the dealer's hand)."""
        # Determine the outcome of the hand against the dealer's if the outcome is unknown
        if not hand.outcome:
            self.determine_hand_outcome(hand, self._dealer.Hand)

        # Perform payout based on the hand outcome
        if hand.outcome == HandOutcome.Win:
            if hand.status == 'Blackjack':
                self._PayOutHand(hand, 'blackjack')
            else:
                self._PayOutHand(hand, 'wager')

        elif hand.outcome == HandOutcome.Push:
            self._PayOutHand(hand, HandOutcome.Push)

        elif hand.outcome == 'Even Money':
            self._PayOutHand(hand, 'wager')

        elif hand.outcome == HandOutcome.InsuranceWin:
            self._PayOutHand(hand, 'insurance')

        elif hand.outcome == HandOutcome.Loss:
            self._AddActivity(f"Hand {hand.hand_number}: Forfeiting hand wager of {money_format(hand.wager)}.")

        else:
            raise ValueError(f"Unhandled hand outcome: {hand.outcome}")

    def _SettleUp(self):
        """For each of the gambler's hands, settle wagers against the dealer's hand."""
        for hand in self._gambler.hands:
            self.settle_hand(hand)

    def track_metrics(self):
        """Update the tracked metrics with the current turn's data."""
        # Track gambler hand metrics
        for hand in self._gambler.hands:
            self.metric_tracker.process_gamblerHand(hand)
        
        # Track dealer hand metrics
        self.metric_tracker.process_dealer_hand(self._dealer.Hand)

        # Track gambler's bankroll through time
        self.metric_tracker.append_bankroll(self._dealer.Bankroll)

    def _FinalizeTurn(self):
        """Clean up the current turn in preparation for the next turn."""
        # Render the final status of the turn if applicable.
        if self.verbose:
            self.render()
        
        # Update tracked metrics
        self.track_metrics()

        # Reset the activity log for the next turn.
        self._activity = []

        # Discard both the gambler and the dealer's hands.
        self._gambler.discard_hands()
        self._dealer.discard_hand()
        
        # Reset hide_dealer for the next turn.
        self.hide_dealer = True

        # Pause exectution until the user wants to proceed if applicable.
        if self.verbose:
            input('Push ENTER to proceed => ')

    def finalize_game(self):
        """Wrap up the game, rendering analytics and creating graphs if necessary."""
        # Render game over message if applicable
        if self.verbose:
            self.render_game_over()
        
    def render(self):
        """Print out the entire game (comprised of table, activity log, and user action) to the console."""
        clear()  # Clear previous rendering
        self.render_table()
        self.render_activity()
        self.render_action()

    def render_table(self):
        """Print out the players and the hands of cards (if they've been dealt)."""

        if self._gambler.AllHands:
            for hand in self._gambler.hands:
                print(hand.pretty_format())
                print()
        else:
            print('No hands.')

    def render_activity(self):
        """Print out the activity log for the current turn."""
        print(header('ACTIVITY'))
        for message in self._activity:
            print(message)

    def render_action(self):
        """Print out the action section that the user interacts with."""
        print(header('ACTION'))
        if self._dealerPlaying:
            print('Dealer playing turn...')

    def render_game_over(self):
        """Print out a final summary message once the game has ended."""
        # Show game over message
        print(header('GAME OVER'))

        # Print a final message after the gambler is finished
        if self._gambler.auto_wager == 0 or self.turn == self.max_turns:
            action = f"{self._gambler.name} cashed out with bankroll: {money_format(self._dealer.Bankroll)}."
            message = 'Thanks for playing!'
        else:
            action = f"{self._gambler.name} is out of money."
            message = 'Better luck next time!'

        print(f"{action}\n\n{message}")
