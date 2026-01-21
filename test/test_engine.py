import unittest

from engine.card import Card
from engine.game_engine import BoerenbridgeEngine

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.player_id = 0
        self.player_0_card = Card(0, 6)
        self.player_1_card = Card(0, 5)
        self.player_2_card = Card(1, 7)
        self.player_3_card = Card(2, 4)

        self.engine = BoerenbridgeEngine()
        self.engine.reset_round(1)

        self.engine.hands = [[self.player_0_card], [self.player_1_card], [self.player_2_card], [self.player_3_card]]
        self.engine.total_score = [0, 0, 0, 0]
        self.engine.trump_suit = 2

        self.engine.make_bet(0, 1)
        self.engine.make_bet(1, 0)
        self.engine.make_bet(2, 0)
        self.engine.make_bet(3, 1)

    def test_play_card(self):
        self.engine.play_card(self.player_id, self.player_0_card)

        assert len(self.engine.hands[self.player_id]) == 0
        assert self.engine.current_trick[self.player_id] == self.player_0_card
        assert self.engine.current_player == self.player_id + 1

    def test_determine_trick_winner(self): 
        self.engine.play_card(self.player_id, self.player_0_card)
        self.engine.play_card(self.player_id + 1, self.player_1_card)
        self.engine.play_card(self.player_id + 2, self.player_2_card)
        
        assert self.engine.is_round_over() == False
        
        self.engine.play_card(self.player_id + 3, self.player_3_card)

        assert len(self.engine.hands[self.player_id]) == 0
        assert self.engine.current_player == 3
        assert self.engine.trick_number == 1
        assert self.engine.trump_suit == 2
        assert self.engine.is_round_over() == True
        assert self.engine.tricks_won == [0, 0, 0, 1]

    def test_make_bet(self):
        assert self.engine.bets[0] == 1 
        self.assertRaises(Exception, self.engine.make_bet, 0, 1)
        self.assertRaises(Exception, self.engine.make_bet, 3, 2)

    def test_resolve_final_score(self):
        self.engine.play_card(self.player_id, self.player_0_card)
        self.engine.play_card(self.player_id + 1, self.player_1_card)
        self.engine.play_card(self.player_id + 2, self.player_2_card)      
        self.engine.play_card(self.player_id + 3, self.player_3_card)

        assert self.engine.is_round_over() == True
        assert self.engine.round_points == [-1, 10, 10, 11]        

    def test_legal_actions_trump_suit(self):
        self.engine.trump_suit = 0
        self.engine.hands[0].append(Card(0, 7))
        self.engine.hands[1].append(Card(0, 8))
        self.engine.hands[2].append(Card(0, 9))
        self.engine.hands[3].append(Card(3, 4))
        self.engine.cards_per_player = 2

        assert self.engine.legal_actions(self.player_id) == self.engine.hands[0]

    def test_legal_actions_no_trump_suit(self):
        self.engine.trump_suit = 4
        self.engine.hands[0].append(Card(0, 7))
        self.engine.hands[1].append(Card(0, 8))
        self.engine.hands[2].append(Card(0, 9))
        self.engine.hands[3].append(Card(3, 4))
        self.engine.cards_per_player = 2

        assert self.engine.legal_actions(self.player_id) == self.engine.hands[0]
        self.engine.play_card(self.player_id, self.player_0_card)
        assert self.engine.legal_actions(self.player_id + 1) == self.engine.hands[1]
        assert self.engine.legal_actions(self.player_id + 2) == [Card(0, 9)]
        assert self.engine.legal_actions(self.player_id + 3) == self.engine.hands[3] 

    def test_all_bets_made(self):
        assert self.engine.all_bets_made()

    def test_last_bet_illegal(self):
        self.engine.bets[3] = None
        self.assertRaises(Exception, self.engine.make_bet, 3, 0)

if __name__ == "__main__":
    unittest.main()
