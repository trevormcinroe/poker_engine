"""

"""

import numpy as np


class Board:

    def __init__(self, deck):

        self.current_board = {
            'suits': [],
            'cards': []
        }
        self.deck = deck

    def next_card(self):
        """"""

        suit, card = self.deck.draw_card()

        self.current_board['suits'].append(suit)
        self.current_board['cards'].append(card)

