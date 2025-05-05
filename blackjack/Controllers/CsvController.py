
import logging
from blackjack.values.CardSuit import CardSuit

class CsvController:

    #get the card format for checking against the csv file
    def GetCardFormat(self, card):
        return card.Rank
    