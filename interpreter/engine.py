"""
Given two hands and a board, which hand is currently ahead?
"""

import numpy as np


class InterpreterEngine:

    def __init__(self):

        self.hand_strength = {
            'high card': 0,
            'one pair': 1,
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


    def _face_card_translate(self, hands, board):
        """To make hand comparisons easier, we want to translate all face cards
        into a numerical representation. This allows for logical comparisons
        such as {>, <, ==} and the like.

        Args:
            hands:
            board:

        Returns:

        """

        # For this process, we take advantage of Python's built-in
        # list comprehension capabilities. We add in a simple if-else
        # statement to check if each item in the given dictionaries
        # exists within the list of facecards
        translated_hands = []

        for hand in hands:

            holder_cards = [
                self.face_card_translator[x]
                if x in list(self.face_card_translator.keys()) else x
                for x in hand['cards']
            ]

            holder_hand = {
                'cards': holder_cards,
                'suits': hand['suits']
            }

            translated_hands.append(holder_hand)

        board['cards'] = [
            self.face_card_translator[x]
            if x in list(self.face_card_translator.keys()) else x
            for x in board['cards']
        ]

        return translated_hands, board

    def compare_hands(self, hands, board):
        """

        Args:
            hands:
            board:

        Returns:

        """

        # First, translating any facecards into their respective
        # numerical representation
        hands, board = self._face_card_translate(hands=hands, board=board)

        # Gathering informaiton about the board
        suit_counts = {
            x: board['suits'].count(x)
            for x in board['suits']
        }

        card_counts = {
            x: board['cards'].count(x)
            for x in board['cards']
        }

        # Now, simply looping through each hand and determining what they have
        hand_results = []
        for hand in hands:
            result1, result2 = self.hand_interpret(hand=hand,
                                                   board=board,
                                                   suit_counts=suit_counts,
                                                   card_counts=card_counts)
            hand_results.append((result1, result2))

        # Now, determining which hand has the strength value...
        hand_strengths = [self.hand_strength[x[0]] for x in hand_results]

        # Now that we have a list of hand strengths, we should check to see if there is a global max
        # If there is, return the hand number, the hand dict itself, and the hand type that was one with
        if len([x for x in hand_strengths if x == np.max(hand_strengths)]) == 1:
            hand_number = hand_strengths.index(np.max(hand_strengths))
            winning_hand = hands[hand_number]
            hand_type = hand_results[hand_number][0]
            return [hand_number], winning_hand, hand_type # we post hand_number as a list to help with ties

        # If there are 2 or more hands with the same strength, we need to look into some tie-breaking...
        else:
            # First, let's the type of hand that is the strongest
            hand_type = [k for k, v in self.hand_strength.items() if v == np.max(hand_strengths)][0]

            # Because we need to retain info about all hand indexes, we need to have a way to
            # reference the main set all of hands while also being able to reference the tied
            # hands at the top whenever we need to
            remaining_hand_indexes = [
                x for x in range(len(hands))
                if hand_strengths[x] == np.max(hand_strengths)
            ]

            #################
            # HAND BREAKOUT #
            #################
            if hand_type == 'quads':
                # (0) The first thing we should be checking for is if any of the players have
                # HIGHER quads than the others
                quad_results = [
                    hand_results[x][1] for x in
                    remaining_hand_indexes
                ]
                highest_quads = np.max(quad_results)

                if not np.mean(quad_results) == highest_quads:
                    hand_number = [
                        x for x in remaining_hand_indexes
                        if highest_quads in hands[x]['cards']
                    ]
                    winning_hand = [
                        hands[x] for x
                        in hand_number
                    ]
                    hand_type = 'quads'
                    return hand_number, winning_hand, hand_type


                # The only possible way that there can be non-tied quads is that one player has
                # a hand card that is BOTH higher than the other player's hand cards AND higher
                # than the highest, non-quad card on the board
                remaining_board = [
                    board['cards'][x] for x in range(len(board['cards']))
                    if board['cards'][x] != hand_results[remaining_hand_indexes[0]][1]
                ]

                # Creating a list of all hand cards that are non-quad cards
                # Here, we loop through each hand, each card in each hand, and append the highest
                # card in the hand. This will allow us to index the list of hands to select as the winner
                remaining_hand_cards = []
                for idx in remaining_hand_indexes:
                    holder = []
                    for c in hands[idx]['cards']:
                        if c > np.max(remaining_board):
                            holder.append(c)
                        else:
                            continue
                    remaining_hand_cards.append(holder)

                # (1) If remaining_hand_cards list is full of empty lists, then there is a tie,
                # as the highest board card is shared amongst all of the players
                if False not in [len(x) == 0 for x in remaining_hand_cards]:
                    # If here, we need to subset the remaining_hand_indexes that
                    hand_number = remaining_hand_indexes
                    winning_hand = [
                        hands[x] for x in range(len(hands))
                        if x in hand_number
                    ]
                    hand_type = 'quads'
                    return hand_number, winning_hand, hand_type

                else:
                    # If here, then there is at least 1 hand that has a higher
                    # First, finding the higest number in remaining_hand_cards
                    unlisted = []
                    for l in remaining_hand_cards:
                        for i in l:
                            unlisted.append(i)
                    highest_card = np.max(unlisted)

                    hand_number = [
                        x for x in remaining_hand_indexes
                        if highest_card in hands[x]['cards']
                    ]

                    winning_hand = [
                        hands[x] for x in remaining_hand_indexes
                        if x in hand_number
                    ]

                    hand_type = 'quads'
                    return hand_number, winning_hand, hand_type

            if hand_type == 'full house':
                # The return from full house is ['full house', (trips, pair)]
                fh_results = [
                    hand_results[x][1]
                    for x in remaining_hand_indexes
                ]
                max_fh = np.max([x[0] for x in [y for y in fh_results]])

                if len([x for x in remaining_hand_indexes if max_fh in hands[x]['cards']]) == 1:
                    # We are here in the logic flow if only a sinlge hand is dominant
                    hand_number = [
                        x for x in remaining_hand_indexes
                        if max_fh in hands[x]['cards']
                    ]
                    winning_hand = [hands[x] for x in hand_number]
                    return hand_number, winning_hand, 'full house'

                else:
                    # If we have reached here in the logic flow, there is at least one player
                    # that has a higher full house than the others. Let us extract them
                    hand_number_trips = [
                        x for x in remaining_hand_indexes
                        if max_fh in hands[x]['cards']
                    ]

                    # Now there should be a check in the pairs.
                    max_pair = np.max([x[1] for x in [y for y in [fh_results[z] for z in hand_number_trips]]])
                    hand_number = [
                        x for x in hand_number_trips
                        if max_pair in hands[x]['cards']
                    ]
                    winning_hand = [hands[x] for x in hand_number]
                    return hand_number, winning_hand, 'full house'

            if hand_type == 'flush':
                pass

            if hand_type == 'straight':
                pass

            if hand_type == 'trips':
                pass

            if hand_type == 'two pair':
                pass

            if hand_type == 'one pair':
                pass

            if hand_type == 'high card':
                pass


        return hand_strengths

    def hand_interpret(self, hand, board, suit_counts, card_counts):
        """"""

        if self._check_quads(hand=hand, board=board, card_counts=card_counts)[0]:
            result = 'quads'
            _, card = self._check_quads(hand=hand, board=board, card_counts=card_counts)
            return result, card

        elif self._check_fullhouse(hand=hand, board=board, card_counts=card_counts)[0]:
            result = 'full house'
            _, trips, pair = self._check_fullhouse(hand=hand, board=board, card_counts=card_counts)
            return result, (trips, pair)

        elif self._check_flush(hand=hand, board=board, suit_counts=suit_counts)[0]:
            result = 'flush'
            _, suit, high_card = self._check_flush(hand=hand, board=board, suit_counts=suit_counts)
            return result, (suit, high_card)

        elif self._check_straight(hand=hand, board=board)[0]:
            result = 'straight'
            _, high_card = self._check_straight(hand=hand, board=board)
            return result, high_card

        elif self._check_trips(hand=hand, board=board, card_counts=card_counts)[0]:
            result = 'trips'
            _, trips = self._check_trips(hand=hand, board=board, card_counts=card_counts)
            return result, trips

        elif self._check_two_pair(hand=hand, board=board, card_counts=card_counts)[0]:
            result = 'two pair'
            _, high_pair, low_pair = self._check_two_pair(hand=hand, board=board, card_counts=card_counts)
            return result, (high_pair, low_pair)

        elif self._check_pair(hand=hand, board=board, card_counts=card_counts)[0]:
            result = 'one pair'
            _, pair = self._check_pair(hand=hand, board=board, card_counts=card_counts)
            return result, pair

        else:
            result = 'high card'
            high_card = self._high_card(hand=hand, board=board)
            return result, high_card
    
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
        if 2 in [v for k, v in card_counts.items()] and len(np.unique(hand['cards'])) == 1:

            # Pulling out a list of the paired cards in the board, then checking to see if the given hand is a pair
            # that combines with one of the pairs on the board
            board_pairs = []

            for card in board['cards']:
                if card_counts[card] == 2 and card not in board_pairs:
                    board_pairs.append(card)

            if np.unique(hand['cards'])[0] in board_pairs:
                return True, np.unique(hand['cards'])[0]
            else:
                return False, None

        # (2) Trips on board, last card in hand
        elif 3 in [v for k, v in card_counts.items()]:

            # Pulling out a list of the trip cards in the board, then checking to see if any of the cards
            # in the given hand are the trip cards on the board
            board_trips = []

            for card in board['cards']:
                if card_counts[card] == 3 and card not in board_trips:
                    board_trips.append(card)

            if len([x for x in hand['cards'] if x in board_trips]) == 0:
                return False, None
            # else:
            for hc in hand['cards']:
                if hc in board_trips:
                    return True, hc
                else:
                    continue
            # return False, None

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

            # There are four possibilities here:
            # (a) The hand misses the board and therefore plays the board
            # (b) The hand connects with the board but the hand's trips are < board's trips
            # (c) The hand connects with the board and the hand's trips are > board's trips
            # (d) The hand also has a pair

            # (d)
            if len(np.unique(hand['cards'])) == 1:
                trips = self._most_common(lst=board['cards'])

                if np.unique(hand['cards'])[0] > [k for k, v in card_counts.items() if v == 2][0]:
                    pair = hand['cards'][0]
                else:
                    pair = [k for k, v in card_counts.items() if v == 2][0]
                return True, trips, pair

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

        # (3) Trips on board:
        elif 3 in [v for k, v in card_counts.items()]:

            # (a) pair in hand
            if len(np.unique(hand['cards'])) == 1:

                # (i) Pair does not connect with board
                if not hand['cards'][0] in board['cards']:

                    # No need to check anything about the pair on the board. This behavior should already be
                    # filtered out above...
                    trips = self._most_common(lst=board['cards'])
                    pair = hand['cards'][0]
                    return True, trips, pair

                # (ii) Pair connects with the board. Need to check if the connected is higher
                else:

                    if hand['cards'][0] > self._most_common(lst=board['cards']):
                        trips = hand['cards'][0]
                        pair = self._most_common(lst=board['cards'])
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

            else:
                return False, None, None

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

        # (4) Double paired board
        elif len([k for k, v in card_counts.items() if v == 2]) == 2:

            # (a) One of the two in hand
            # (b) Both in hand (need to take higher one as trips)
            # (C) totall misses

            # (c)
            if [x in [k for k, v in card_counts.items() if v == 2] for x in hand['cards']].count(True) == 0:
                return False, None, None

            # (a)
            if [x in board['cards'] for x in hand['cards']].count(True) == 1:

                # (i) The board pair that the hand connected with is higher than the non-connected
                if np.max([k for k, v in card_counts.items() if v == 2]) in hand['cards']:
                    trips = np.max([k for k, v in  card_counts.items() if v == 2])
                    pair = [k for k, v in  card_counts.items() if v == 2 and k not in hand['cards']][0]
                    return True, trips, pair

                # (ii) The board pair that the hand connected with is lower than the non-connected
                if not np.max([k for k, v in  card_counts.items() if v == 2]) in hand['cards']:
                    pair = np.max([k for k, v in  card_counts.items() if v == 2])
                    trips = [k for k, v in  card_counts.items() if v == 2 and k != pair][0]
                    return True, trips, pair

            if [x in board['cards'] for x in hand['cards']].count(True) == 2:

                # Some weird logic gate here: we can run into the issue where one card in the hand
                # connects with a pair on the board and the other connects with a non-pair on the board

                # If both cards in the hand connect to board pairs,
                # then simply return the higher one as the trips, lower as pair
                if [x in [k for k, v in card_counts.items() if v == 2] for x in hand['cards']].count(True) == 2:
                    trips = np.max(hand['cards'])
                    pair = [x for x in hand['cards'] if x != trips][0]
                    return True, trips, pair

                else:

                    # Two cases here:
                    # (a) Pair made between hand and board is > non-trip board pair
                    # (b) Pair made between hand and board is < non-trip board pair

                    trips = [x for x in hand['cards'] if x in [k for k, v in card_counts.items() if v == 2]][0]
                    non_trips_hand_card = [x for x in hand['cards'] if x != trips][0]
                    # (a)
                    if non_trips_hand_card > [k for k, v in card_counts.items() if v == 2 and k != trips][0]:
                        pair = non_trips_hand_card
                    # (b)
                    else:
                        pair = [k for k, v in card_counts.items() if v == 2 and k != trips][0]
                    return True, trips, pair

        # (5) One pair board and other
            if [k for k, v in card_counts.items() if v == 2][0] in hand['cards']:
                if len([x for x in hand['cards'] if x in [k for k, v in card_counts.items() if v != 2]]):
                    return True, \
                           [k for k, v in card_counts.items() if v == 2][0], \
                           [x for x in hand['cards'] if x in [k for k, v in card_counts.items() if v != 2]][0]
            else:
                return False, None, None
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

    def _check_straight(self, hand, board):
        """

        Args:
            hand:
            board:

        Returns:
            Bool for existence, high card if exists
        """

        # First, let's connect the list of the hand and the board and then make them in descending order
        all_cards = board['cards'] + hand['cards']
        all_cards = list(np.unique(all_cards))
        all_cards.sort(reverse=True)

        # If there is an ace in the list, this should be handled in a special way...
        if 14 in all_cards:

            # (1) Checking for face-card flush
            # Subtracting each card's value by the card after it
            # If a straight exists, there should be a slice of four 1's
            sequential_check = [all_cards[x] - all_cards[x+1] for x in range(len(all_cards) - 1)]

            # To find this, we will create a sliding window across sequential_check
            x_beg = 0
            x_end = 3

            while x_end < len(sequential_check):
                if np.mean(sequential_check[x_beg: x_end + 1]) == 1:
                    return True, np.max(all_cards[x_beg: x_end+1])

                x_beg += 1
                x_end += 1

            # (2) Checking for the wheel
            # To do so, we reassign 14 to 1 and resort the list
            all_cards[all_cards.index(14)] = 1
            all_cards.sort(reverse=True)

            # Subtracting each card's value by the card after it
            # If a straight exists, there should be a slice of four 1's
            sequential_check = [all_cards[x] - all_cards[x+1] for x in range(len(all_cards) - 1)]

            # To find this, we will create a sliding window across sequential_check
            x_beg = 0
            x_end = 3

            while x_end < len(sequential_check):
                if np.mean(sequential_check[x_beg: x_end + 1]) == 1:
                    return True, np.max(all_cards[x_beg: x_end+1])

                x_beg += 1
                x_end += 1

            return False, None

        else:
            # Subtracting each card's value by the card after it
            # If a straight exists, there should be a slice of four 1's
            sequential_check = [all_cards[x] - all_cards[x+1] for x in range(len(all_cards) - 1)]

            # To find this, we will create a sliding window across sequential_check
            x_beg = 0
            x_end = 3

            while x_end < len(sequential_check):
                if np.mean(sequential_check[x_beg: x_end+1]) == 1:
                    return True, np.max(all_cards[x_beg: x_end+1])

                x_beg += 1
                x_end += 1

            return False, None

    def _check_trips(self, hand, board, card_counts):
        """
        
        Args:
            hand: 
            board: 
            card_counts: 

        Returns:
            Bool for existence, trips card if exists
        """

        # (1) Simply flopped trips
        if len(np.unique(hand['cards'])) == 1:

            # (a) Board could have trips
            if 3 in [v for k, v in card_counts.items()]:

                # (i) Flopped set > board trips
                if hand['cards'][0] > [k for k, v in card_counts.items() if v == 3][0]:
                    return True, hand['cards'][0]
                # (ii) Flopped set < board trips
                else:
                    return True, [k for k, v in card_counts.items() if v == 3][0]

            if hand['cards'][0] in board['cards']:
                return True, hand['cards'][0]

        # (2) Board can have trips
        if 3 in [v for k, v in card_counts.items()]:

            # (a) Flopped trips -- we can again abuse the logic flow. No need to check for quads
            if len(np.unique(hand['cards'])) == 1 and np.unique(hand['cards'])[0] in board['cards']:

                # (i) Flopped trips > board trips
                if hand['cards'][0] > [k for k, v in card_counts.items() if v == 3][0]:
                    return True, hand['cards'][0]

                # (ii) Flopped trips < board trips
                else:
                    return True, [k for k, v in card_counts.items() if v == 3][0]

            # (b) Not flopped trips
            else:

                # (i) Board is also paired
                if 2 in [v for k, v in card_counts.items() if v == 2]:
                    if True in [x in [k for k, v in card_counts.items() if v == 2] for x in hand['cards']]:
                        hand_to_board = [x for x in hand['cards'] if x in [k for k, v in card_counts.items() if v ==2]]

                        # Now we have to check to see if the connected trips are > or < board trips
                        if hand_to_board > [k for k, v in card_counts.items() if v == 3][0]:
                            return True, hand_to_board[0]
                        else:
                            return True, [k for k, v in card_counts.items() if v == 3][0]
                else:
                    return True, [k for k, v in card_counts.items() if v == 3][0]

        # (3) Board has a pair
        if 2 in [v for k, v in card_counts.items()]:

            # Now, one of the cards in given hand must be one of the pairs
            if True in [x in [k for k, v in card_counts.items() if v == 2] for x in hand['cards']]:
                all_trips = [x for x in hand['cards'] if x in [k for k, v in card_counts.items() if v == 2]]
                return True, np.max(all_trips)

            else:
                return False, None

        return False, None

    def _check_two_pair(self, hand, board, card_counts):
        """

        Args:
            hand:
            board:
            card_counts:

        Returns:
            Bool for existence, higher pair if exists, lower pair if exists
        """

        # (1) Board can simply have 2 pairs
        # Again, we are abusing the logic flow in the above method
        if len([k for k, v in card_counts.items() if v == 2]) == 2:

            # (a) the hand could also connect with board. We must then see if this card is higher than the two pairs
            if True not in [x in [k for k, v in card_counts.items()] for x in hand['cards']]:
                return True, \
                       np.max([k for k, v in card_counts.items() if v == 2]), \
                       np.min([k for k, v in card_counts.items() if v == 2])

            else:

                # Gathering a list of all of the pairs...
                pairs_list = [k for k, v in card_counts.items() if v == 2] \
                             + [x for x in hand['cards'] if x in [k for k, v in card_counts.items()] ]

                # Removing the smallest one
                pairs_list.pop(pairs_list.index(np.min(pairs_list)))
                return True, np.max(pairs_list), np.min(pairs_list)

        # (2) Board can have >= one pair and hand can have pair
        if len(np.unique(hand['cards'])) == 1 and len([k for k, v in card_counts.items() if v == 2]) > 0:

            # (a) Paired hand
            if len(np.unique(hand['cards'])) == 1:
                pairs_list = [hand['cards'][0]] + [k for k, v in card_counts.items() if v == 2]
                if len(pairs_list) == 2:
                    return True, np.max(pairs_list), np.min(pairs_list)
                else:
                    pairs_list.pop(pairs_list.index(np.min(pairs_list)))
                    return True, np.max(pairs_list), np.min(pairs_list)

            # (b) no pocket pair
            else:
                if True in [x in [k for k, v in card_counts.items()] for x in hand['cards']]:

                    pairs_list = [k for k, v in card_counts.items() if v == 2] \
                                 + [x for x in hand['cards'] if x in [k for k, v in card_counts.items()]]
                    if len(pairs_list) == 2:
                        return True, np.max(pairs_list), np.min(pairs_list)
                    else:
                        pairs_list.pop(pairs_list.index(np.min(pairs_list)))
                        return True, np.max(pairs_list), np.min(pairs_list)

        # (3) Two hole cards both connect
        if len([x for x in hand['cards'] if x in board['cards']]) == 2:
            return True, np.max(hand['cards']), np.min(hand['cards'])

        # (4) Pair on board and pair between hand and board
        if len([k for k, v in card_counts.items() if v == 2]) == 1:
            if len([x for x in hand['cards'] if x in board['cards']]):
                pairs_list = [x for x in hand['cards'] if x in board['cards']] \
                             + [k for k, v in card_counts.items() if v == 2]
                return True, np.max(pairs_list), np.min(pairs_list)

        return False, None, None

    def _check_pair(self, hand, board, card_counts):
        """

        Args:
            hand:
            board:
            card_counts:

        Returns:
            Bool for existence, card if exists
        """

        # (1) The board can have a single pair
        if len([k for k, v in card_counts.items() if v == 2]) == 1:
            return True, [k for k, v in card_counts.items() if v == 2][0]

        # (2) Pair in the hand
        if len(np.unique(hand['cards'])) == 1:
            return True, hand['cards'][0]

        # (3) Card in hand pairs with board
        if True in [x in board['cards'] for x in hand['cards']]:
            return True, [x for x in hand['cards'] if x in board['cards']][0]

        return False, None

    def _high_card(self, hand, board):
        """

        Args:
            hand:
            board:

        Returns:
            number of highest card
        """

        card_candidates = hand['cards'] + board['cards']
        return np.max(card_candidates)

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

#
# hand_one = {
#     'cards': [3, 'Q'],
#     'suits': ['s', 's']
# }
#
# hand_two = {
#     'cards': ['K', 'K'],
#     'suits': ['s', 'd']
# }
#
# board = {
#     'cards': ['A', 'A', 'K', 7, 5],
#     'suits': ['d', 's', 's', 's', 's']
# }
#
# suit_counts = {
#     x: board['suits'].count(x)
#     for x in board['suits']
# }
#
# a = InterpreterEngine()
#
# print(a.compare_hands(hand_one=hand_one, hand_two=hand_two, board=board))
#
# # print(a._face_card_translate(hand_one=hand_one,
#                        hand_two=hand_two,
#                        board=board)
# )

# print(a._check_flush(hand=hand_one, board=board, suit_counts=suit_counts))

a = InterpreterEngine()
board = {'cards': [11, 11, 10, 'A', 'A'], 'suits': ['c', 's', 's', 'd', 'h']}
hand_one = {'cards': ['A', 10], 'suits': ['s', 'd']}
hand_two = {'cards': [10, 10], 'suits': ['s', 'd']}
hand_three = {'cards': ['J', 'A'], 'suits': ['s', 'd']}

hands = [hand_one, hand_two, hand_three]

print(a.compare_hands(hands=hands, board=board))