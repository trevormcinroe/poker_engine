"""

"""

import numpy as np

class Game:

    """

    """

    def __init__(self, deck, board, small_blind):

        self.deck = deck
        self.board = board
        self.small_blind = small_blind
        self.players = None
        self.remaining_players = None
        self.current_pot = 0
        self.button_position = None
        self.current_betting_round = None
        self.remaining_players = None
        self.small_blind_position = None
        self.big_blind_position = None


    def add_players(self, players):
        """"""

        self.players = players
        self.button_position = np.random.choice([x for x in range(len(self.players))])

    def deal_hand(self):
        """"""

        # (0) Shuffling our deck
        self.deck.shuffle()

        # (1) Looping through each player and giving them one card
        # We accomplish this by creating a list of empty hand dictionaries
        dealt_cards = [
            {
                'cards': [],
                'suits': []
            }
            for _ in range(len(self.players))
        ]

        for _ in range(2):
            for i in range(len(self.players)):
                suit, card = self.deck.draw_card()
                dealt_cards[i]['cards'].append(card)
                dealt_cards[i]['suits'].append(suit)

        # Here, we have a list of hand dictionaries
        # Now, we can simply loop through them and assign them to each of the
        # game's players
        for i in range(len(dealt_cards)):
            self.players[i].current_hand = dealt_cards[i]

    def deal_flop(self):
        """"""
        for _ in range(3):
            suit, card = self.deck.draw_card()
            self.board.add_card(suit=suit, card=card)

    def deal_turn(self):
        """"""
        suit, card = self.deck.draw_card()
        self.board.add_card(suit=suit, card=card)

    def deal_river(self):
        """"""
        suit, card = self.deck.draw_card()
        self.board.add_card(suit=suit, card=card)

    def betting_round(self):
        """"""

        # If we are preflop, each player gets a chance, starting with the UTG
        # position, which is ultimately 3 spots ahead of the button player
        if self.current_betting_round == 'preflop':

            # Pulling out the blinds
            small_b = self.players[self.small_blind_position].bet(amount=self.small_blind)
            big_b = self.players[self.big_blind_position].bet(amount=self.small_blind * 2)
            self.current_pot += small_b
            self.current_pot += big_b

            # Declaring the first betting position
            if self.big_blind_position == len(self.players):
                current_bettor = 0
            else:
                current_bettor = self.big_blind_position + 1

            current_num_bets = 0

            while current_num_bets <= len(self.remaining_players):
                self.players[current_bettor].bet()
                current_num_bets += 1
                if current_bettor == len(self.players):
                    current_bettor = 0
                else:
                    current_bettor += 1


        if self.current_betting_round == 'flop':
            pass

        if self.current_betting_round == 'turn':
            pass

        if self.current_betting_round == 'river':
            pass

        pass

    def move_button(self):
        """A simple method that moves the position of the button.
        The one check deals with the inconvenience of a finite number of
        players
        """

        if self.button_position == len(self.players):
            self.button_position = 0
        else:
            self.button_position += 1

        if self.button_position == len(self.players):
            self.small_blind_position = 0
        else:
            self.small_blind_position += 1

        if self.small_blind_position == len(self.players):
            self.big_blind_position = 0
        else:
            self.big_blind_position += 1



    def hand_completion(self):
        """"""
        pass

    def play_hand(self):
        """"""

        # (0) Dealing cards/resetting remaining players index
        self.deal_hand()
        self.remaining_players = [x for x in range(len(self.players))]

        # (1) Facilitating a betting round
        self.current_betting_round = 'preflop'

        # (2) Dealing the flop
        self.deal_flop()
        self.current_betting_round = 'flop'

        # (3) Facilitating a betting round

        # (4) Dealing the turn
        self.deal_turn()
        self.current_betting_round = 'turn'

        # (5) Facilitating a betting round

        # (6) Dealing the river
        self.deal_river()
        self.current_betting_round = 'river'

        # (7) Facilitating a betting round

        # (9) Finishing up the hands

        # (10) Moving the button
        self.move_button()

