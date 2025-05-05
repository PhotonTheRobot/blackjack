from enum import Enum

class HandOutcome(str, Enum):
    Loss = 0
    Win = 1
    Push = 2
    InsuranceWin = 3
    
    def __repr__(self):
      return self.value