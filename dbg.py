# from card_utils.deck import Deck
# from interpreter.engine import InterpreterEngine
#
#
# I = InterpreterEngine()


# txt = 'y'
#
# while txt == 'y':
#
#     # Init the deck
#     D = Deck()
#
#     # Init both hands
#     hand_one = {
#         'cards': [],
#         'suits': []
#     }
#
#     hand_two = {
#         'cards': [],
#         'suits': []
#     }
#
#     board = {
#         'cards': [],
#         'suits': []
#     }
#
#     # Drawing two cards for the hand
#     for _ in range(2):
#         suit, card = D.draw_card()
#
#         hand_one['cards'].append(card)
#         hand_one['suits'].append(suit)
#
#         hand_two['cards'].append(card)
#         hand_two['suits'].append(suit)
#
#     for _ in range(5):
#         suit, card = D.draw_card()
#
#         board['cards'].append(card)
#         board['suits'].append(suit)
#
#     hand, items = I.compare_hands(hand_one=hand_one,
#                           hand_two=hand_two,
#                           board=board)
#
#     print(f'{board}\n {hand_one} \n {hand} \n {items}')
#     txt = input('Correct?')

from card_utils.deck import Deck
from game_utils.game import Game
from player_utils.player import Player
from board_utils.board import Board

p1 = Player(chips=100)
p2 = Player(chips=100)
p3 = Player(chips=100)
d = Deck()
b = Board()
g = Game(deck=d, board=b)
g.add_players([p1, p2, p3])

g.play_hand()

# g.deal_hand()
#
# for p in g.players:
#     print(p.current_hand)


