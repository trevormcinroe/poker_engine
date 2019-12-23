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
            'quads': 7,
            'straight flush': 8
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
        hand_one['cards'] = [
            self.face_card_translator[x]
            if x in list(self.face_card_translator.keys()) else x
            for x in hand_one['cards']
        ]

        hand_two['cards'] = [
            self.face_card_translator[x]
            if x in list(self.face_card_translator.keys()) else x
            for x in hand_two['cards']
        ]

        board['cards'] = [
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

        # Gathering informaiton about the board
        suit_counts = {
            x: board['suits'].count(x)
            for x in board['suits']
        }

        card_counts = {
            x: board['cards'].count(x)
            for x in board['cards']
        }

        # First finding what the two hands have
        # We'll begin with the first hand...
        # return self._check_quads(hand=hand_one, board=board, card_counts=card_counts)
        return self._check_fullhouse(hand=hand_one, board=board, card_counts=card_counts)
        # return self._check_flush(hand=hand_one, board=board, suit_counts=suit_counts)

    def _check_straight_flush(self, hand, suit_counts, card_counts):
        """"""
        pass

    def _check_quads(self, hand, board, card_counts):
        """

        Args:
            hand:
            board:
            card_counts:

        Returns:
            Bool for existence, card if exists
        """

        if not np.max([v for k, v in card_counts.items()]) > 1:
            return False, None

        # (1) Quads on board
        if np.max([v for k, v in card_counts.items()]) == 4:
            return True, self._most_common(lst=board['cards'])

        # (2) Pair in hand, board paired the same
        elif 2 in [v for k, v in card_counts.items()] and len(np.unique(hand['cards'])) == 1:

            # Pulling out a list of the paired cards in the board, then checking to see if the given hand is a pair
            # that combines with one of the pairs on the board
            board_pairs = []

            for card in board['cards']:
                if card_counts[card] == 2 and not card in board_pairs:
                    board_pairs.append(card)

            if np.unique(hand['cards'])[0] in board_pairs:
                return True, np.unique(hand['cards'])[0]

        # (2) Trips on board, last card in hand
        elif 3 in [v for k, v in card_counts.items()]:

            # Pulling out a list of the trip cards in the board, then checking to see if any of the cards
            # in the given hand are the trip cards on the board
            board_trips = []

            for card in board['cards']:
                if card_counts[card] == 3 and not card in board_trips:
                    board_trips.append(card)

            for hc in hand['cards']:
                if hc in board_trips:
                    return True, hc
                else:
                    continue

        else:
            return False, None

    def _check_fullhouse(self, hand, board, card_counts):
        """

        Args:
            hand:
            suit_counts:
            card_counts:

        Returns:
            Bool for existence, trips if exists, pair if exists
        """

        # In order for a fullhouse to be possible, the board must contain at least one pair
        if not np.max([v for k, v in card_counts.items()]) > 1:
            return False, None, None

        # (1) Board can contain a fullhouse itself
        if 3 in [v for k, v in card_counts.items()] and 2 in [v for k, v in card_counts.items()]:

            # There are three possibilities here:
            # (a) The hand misses the board and therefore plays the board
            # (b) The hand connects with the board but the hand's trips are < board's trips
            # (c) The hand connects with the board and the hand's trips are > board's trips

            # (a)
            if not True in np.unique([x in board['cards'] for x in hand['cards']]):
                # The trips will be the most common and the pair will be the non-most-common
                trips = self._most_common(lst=board['cards'])
                pair = [x for x in board['cards'] if x != trips][0]

                return True, trips, pair

            else:
                # Here in the logic flow, the hand has connected with the board somehow
                # We can simpy use the values of the cards on the board to determine between (b) and (c)
                board_trips = self._most_common(lst=board['cards'])
                board_pair = [x for x in board['cards'] if x != board_trips][0]

                # (b)
                if board_trips > board_pair:
                    return True, board_trips, board_pair
                # (c)
                else:
                    return True, board_pair, board_trips

        # Every other fullhouse possibility requires a pair to be in the given hand
        # if not len(np.unique(hand['cards'])) == 1:
        #     return False, None, None

        # (2) Pair in hand that connects with the board AND board has a pair
        elif len(np.unique(hand['cards'])) == 1 and np.unique(hand['cards'])[0] in board['cards']:

            # Here in the logic flow, there are two possibilities;
            # (a) The board only has one pair
            # (b) the board has two pairs

            # (a)
            # In this case, we do not need to check for the higher pair
            if len([k for k, v in card_counts.items() if v == 2]) == 1:
                trips = np.unique(hand['cards'])[0]
                pair = self._most_common(lst=board['cards'])
                return True, trips, pair

            # (b)
            # In this case, however, we need to check to see which pair is higher
            else:
                trips = np.unique(hand['cards'])[0]
                pair = np.max([k for k, v in card_counts.items() if v == 2])
                return True, trips, pair

        # (3) Trips on board:
        elif 3 in [v for k, v in card_counts.items()]:

            # (a) pair in hand
            if len(np.unique(hand['cards'])) == 1:

                # (i) Pair does not connect with board
                if not hand['cards'][0] in board['cards']:
                    trips = self._most_common(lst=board['cards'])
                    pair = hand['cards'][0]
                    return True, trips, pair

                # (ii) Pair connects with the board. Need to check if the connected is higher
                else:
                    if hand['cards'][0] > self._most_common(lst=board['cards']):
                        trips = hand['cards'][0]
                        pair = self._most_common(lst=['board'])
                        return True, trips, pair

                    else:
                        trips = self._most_common(lst=board['cards'])
                        pair = hand['cards'][0]
                        return True, trips, pair

            # (b) pair between hand and board
            elif True in [x in board['cards'] for x in hand['cards']]:
                trips = self._most_common(lst=board['cards'])
                pair = np.max([x for x in hand['cards'] if x in board['cards']])
                return True, trips, pair



        # (4) Double paired board
        elif len([k for k, v in card_counts.items() if v == 2]) == 2:

            # (a) One of the two in hand
            # (b) Both in hand (need to take higher one as trips)
            # (C) totall misses

            # (c)
            if len([x in board['cards'] for x in hand['cards']].count(True)) == 0:
                return False, None, None

            # (a)
            if len([x in board['cards'] for x in hand['cards']].count(True)) == 1:

                # (i) The board pair that the hand connected with is higher than the non-connected
                if np.max([k for k, v in board['cards'].items() if v == 2]) in hand['cards']:
                    trips = np.max([k for k, v in board['cards'].items() if v == 2])
                    pair = [k for k, v in board['cards'].items() if v == 2 and k not in hand['cards']][0]
                    return True, trips, pair

                # (ii) The board pair that the hand connected with is lower than the non-connected
                if not np.max([k for k, v in board['cards'].items() if v == 2]) in hand['cards']:
                    pair = np.max([k for k, v in board['cards'].items() if v == 2])
                    trips = [k for k, v in board['cards'] if v == 2 and k != pair]
                    return True, trips, pair

            if len([x in board['cards'] for x in hand['cards']].count(True)) == 2:

                # If both cards in the hand connect, then simply return the higher one as the trips, lower as pair
                trips = np.max(hand['cards'])
                pair = [x for x in hand['cards'] if x != trips][0]
                return True, trips, pair

        else:
            return False, None, None

    def _check_flush(self, hand, board, suit_counts):
        """

        Args:
            hand:
            board:
            suit_counts:

        Returns:
            Bool for existence, suit if exists, high card if exists
        """

        # Gathering some quick information about the most common suit on the board
        max_suit_cnt = np.max([v for k, v in suit_counts.items()])

        # There must be more than two of a suit for a flush to be possible
        if not max_suit_cnt > 2:
            return False, None, None

        # Now that we have determined that a flush is possible via the board,
        # Lets determine if the two given hands also allow for it...
        # 3 board, 2 hand
        if max_suit_cnt == 3:
            if not len(np.unique(hand['suits'])) == 1:
                return False, None, None

            # If we are here in the logic flow, the board contains 3 of the
            # same suit and the hand has two of the same suit. All that is left
            # to do now is check whether or not these two groups are the same
            # suit...
            if self._most_common(lst=board['suits']) == np.unique(hand['suits']):
                return True, \
                       np.unique(hand['suits'])[0], \
                       self._flush_high_card(hand=hand, board=board, suit=self._most_common(lst=board['suits']))
            else:
                return False, None, None

        # 4 board, 1 hand
        elif max_suit_cnt == 4:

            # Here in the logic flow, we have determined that the board has 4 of the same suit on it
            # In this case, there need only be one of the suit in the hand of the player
            if self._most_common(lst=board['suits']) in hand['suits']:
                return True, \
                       self._most_common(lst=board['suits']), \
                       self._flush_high_card(hand=hand, board=board, suit=self._most_common(lst=board['suits']))

            else:
                return False, None, None

        # The final way is a flush on the board
        elif max_suit_cnt == 5:
            return True, \
                   self._most_common(lst=board['suits']), \
                   self._flush_high_card(hand=hand, board=board, suit=self._most_common(lst=board['suits']))

        else:
            return False, None, None

    def _check_straight(self, hand, suit_counts, card_counts):
        """"""
        pass

    def _check_trips(self, hand, suit_counts, card_counts):
        """"""
        pass

    def _check_two_pair(self, hand, suit_counts, card_counts):
        """"""
        pass

    def _check_pair(self, hand, suit_counts, card_counts):
        """"""
        pass

    def _most_common(self, lst):
        """A simple utility to find the most common item in a list"""
        return max(set(lst), key=lst.count)

    def _flush_high_card(self, hand, board, suit):
        """A utility that will find the high card in a flush

        Args:
            hand (dict):
            board (dict):

        Returns:
            the high card of the flush
        """

        # The first thing we need to do is subset our lists of cards to only those that have the proper suit
        # To do this, we take advantage of the compact
        board_cards = [
            board['cards'][ind] for ind
            in [i for i, x in enumerate(board['suits']) if x == suit]
        ]

        hand_cards = [
            hand['cards'][ind] for ind
            in [i for i, x in enumerate(hand['suits']) if x == suit]
        ]

        # Now concatenating the two lists together
        [board_cards.append(x) for x in hand_cards]

        # Returning the max number
        return np.max(board_cards)

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
    'cards': [2, 8],
    'suits': ['s', 's']
}

hand_two = {
    'cards': ['K', 'K'],
    'suits': ['s', 'd']
}

board = {
    'cards': [5, 5, 5, 8, 8],
    'suits': ['d', 's', 's', 's', 's']
}

suit_counts = {
    x: board['suits'].count(x)
    for x in board['suits']
}

a = InterpreterEngine()

print(a.compare_hands(hand_one=hand_one, hand_two=hand_two, board=board))

# print(a._face_card_translate(hand_one=hand_one,
#                        hand_two=hand_two,
#                        board=board)
# )

# print(a._check_flush(hand=hand_one, board=board, suit_counts=suit_counts))