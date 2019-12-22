"""
Given two hands and a board, which hand is currently ahead?
"""

import numpy as np


class InterpreterEngine:

    def __init__(self):

        self.hand_strength = {
            'high card': 0,
            'pair': 1,
            'two pair': 2,
            'trips': 3,
            'straight': 4,
            'flush': 5,
            'full house': 6,
            'straight flush': 7
        }

        self.face_card_translator = {
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }


    def hand_compare(self, hand_one, hand_two, board):
        """"""

        # Gathering informaiton about the board
        suit_counts = {
            x: board['suits'].count(x)
            for x in board['suits']
        }

        card_counts = {
            x: board['cards'].count(x)
            for x in board['cards']
        }

        ################
        ##### FLUSH ####
        ################
        flush_possible = True

        while flush_possible:

            # If there is a suit with more than 2 occurances in the board,
            # Then we need to check for the possibility of a flush
            if not np.max([v for k, v in suit_counts.items()]) > 2:
                flush_possible = False

            # Now there are two possible ways to make a flush
            # 3 board, 2 hand

            # 4 board, 1 hand
            pass

        ################
        ## FULL HOUSE ##
        ################
        fh_possible = True

        while fh_possible:

            # The board must be at least paired for a FH to be possible
            if np.max([v for k, v in card_counts.items()]) < 2:
                fh_possible = False


        ################
        ### STRAIGHT ###
        ################
        straight_possible = True

        while straight_possible:

            pass

        ################
        ### TWO PAIR ###
        ################
        two_pair_possible = True

        while two_pair_possible:

            pass

        ################
        ### ONE PAIR ###
        ################
        one_pair_possible = True

        while one_pair_possible:

            pass





a = [1, 1, 2, 3, 3, 3, 4]

b = {x: a.count(x) for x in a}

print(b)
