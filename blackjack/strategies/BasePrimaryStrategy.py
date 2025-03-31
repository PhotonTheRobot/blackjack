from abc import ABC, abstractmethod


class BasePrimaryStrategy(ABC):
    @abstractmethod
    def GetWager(self, count):
        """Get a new auto-wager amount (float)."""
