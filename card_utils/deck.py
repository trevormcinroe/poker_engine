"""

"""

import numpy as np
import copy


class Deck:

    def __init__(self):

        self.all_cards = {
            'd': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'],
            'h': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'],
            's': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'],
            'c': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        }

        self.current_cards = None

        self._create()


    def _create(self):
        """"""

        self.current_cards = copy.deepcopy(self.all_cards)

    def draw_card(self):
        """"""

        # Selecting the suit and the card number
        suit = np.random.choice(list(self.current_cards.keys()))
        card = np.random.choice(self.current_cards[suit])

        # For whatever reason, using the above functions make the selections into strings...
        try:
            card = int(card)
        except:
            pass

        # Now we need to remove the chosen card from the current deck
        self.current_cards[suit].remove(card)

        return suit, card

