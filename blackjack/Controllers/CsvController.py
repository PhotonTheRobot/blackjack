
import logging
from blackjack.values.CardSuit import CardSuit

class CsvController:
    
    _logger = None
    
    def __init__(self ):
        self._logger = logging.getLogger(__name__)
        self._logger.debug("CsvController initialized.")
      
    #get the card format for checking against the csv file
    def GetCardFormat(self, card):
        return card.Rank
    