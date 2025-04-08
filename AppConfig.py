
def GetAppConfig():
    """Get game configuration data for the simulation game mode."""
    return {
        'gambler': {
            'bankroll': 10000,   
            'trueCountChipMultiplier': 25
        },
        'table': {
            'numberOfDecks': 6,
            'penetration': 1.0,
            'minBet': 15,   
            'maxBet': 1000,
            'dealerStandOnSoft17': True,
            'doubleAfterSplitAllowed': True,
            'maximumSplitsAllowed': 3,
            'surrenderAllowed': True,
            'blackjackPayout': 1.5,
            'insurancePayout': 2.0,
            'doublePayout': 2.0,
            'surrenderPayout': 0.5,
        },
        'gameplay': {
            'maxTurnsPerIteration': 1000,
            'maxIterations': 1000,
            'logLevel': 'DEBUG',
        }
    }
