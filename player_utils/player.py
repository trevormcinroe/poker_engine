"""

"""

import numpy as np


class Player:
    """

    """

    def __init__(self,
                 chips):
        self.chips = chips
        self.current_hand = None

    def check(self):
        """"""
        pass

    def bet(self, amount):
        """"""

        # If the amount of the given bet is more than the player's current chips, what do we do?
        # In GUI-based poker applications, the GUI does not allow the player to select a bet size that is more
        # then the amount of chips in their current stack.
        # TODO: correct course
        if amount > self.chips:
            raise ValueError('Bet amount cannot be greater than current stack size.')

        self.chips -= amount

        return amount


    def fold(self):
        """"""
        pass
