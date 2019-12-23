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


    def _face_card_translate(self, hand_one, hand_two, board):
        """To make hand comparisons easier, we want to translate all face cards
        into a numerical representation. This allows for logical comparisons
        such as {>, <, ==} and the like.

        Args:
            hand_one:
            hand_two:
            board:

        Returns:

        """

        # For this process, we take advantage of Python's built-in
        # list comprehension capabilities. We add in a simple if-else
        # statement to check if each item in the given dictionaries
        # exists within the list of facecards
        hand_one = [
            self.face_card_translator[x]
            if x in list(self.face_card_translator.keys()) else x
            for x in hand_one['cards']
        ]

        hand_two = [
            self.face_card_translator[x]
            if x in list(self.face_card_translator.keys()) else x
            for x in hand_two['cards']
        ]

        board = [
            self.face_card_translator[x]
            if x in list(self.face_card_translator.keys()) else x
            for x in board['cards']
        ]

        return hand_one, hand_two, board

    def compare_hands(self, hand_one, hand_two, board):
        """

        Args:
            hand_one:
            hand_two:
            board:

        Returns:

        """

        # First, translating any facecards into their respective
        # numerical representation
        hand_one, hand_two, board = self._face_card_translate(
            hand_one=hand_one,
            hand_two=hand_two,
            board=board
        )

        # First finding what the two hands have
        first_hand = self._analyze_hand(hand=hand_one, board=board)
        second_hand = self._analyze_hand(hand=hand_two, board=board)

    def _check_straight_flush(self, hand, board):
        """"""
        pass

    def _check_fullhouse(self, hand, board):
        """"""
        pass

    def _check_flush(self, hand, board):
        """"""
        pass

    def _check_straight(self, hand, board):
        """"""
        pass

    def _check_trips(self, hand, board):
        """"""
        pass

    def _check_two_pair(self, hand, board):
        """"""
        pass

    def _check_pair(self, hand, board):
        """"""
        pass



    def _analyze_hand(self, hand, board):
        """

        Args:
            hand:
            board:

        Returns:

        """

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
            max_suit_cnt = np.max([v for k, v in suit_counts.items()])

            if not max_suit_cnt > 2:
                flush_possible = False

            # Now that we have determined that a flush is possible via the board,
            # Lets determine if the two given hands also allow for it...
            # 3 board, 2 hand
            if max_suit_cnt == 3:
                if not len(np.unique(hand['suits'])) == 1:
                    flush_possible = False

                # If we are here in the logic flow, the board contains 3 of the
                # same suit and the hand has two of the same suit. All that is left
                # to do now is check whether or not these two groups are the same
                # suit...


            # 4 board, 1 hand
            if max_suit_cnt == 4:
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





hand_one = {
    'cards': [2, 'J'],
    'suits': ['s', 's']
}

hand_two = {
    'cards': ['K', 'K'],
    'suits': ['s', 'd']
}

board = {
    'cards': ['A', 'Q'],
    'suits': ['s', 's']
}

a = InterpreterEngine()

print(a._face_card_translate(hand_one=hand_one,
                       hand_two=hand_two,
                       board=board)
)