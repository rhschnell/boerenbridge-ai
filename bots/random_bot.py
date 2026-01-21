import random

class Bot:
    def __init__(self, player_id, rng=None):
        self.player_id = player_id
        self.rng = rng or random.Random()

    def make_bet(self, engine):
        max_bet = engine.cards_per_player
        return self.rng.randint(0, max_bet)
    
    def play_card(self, engine):
        cards = engine.legal_actions(self.player_id)
        return self.rng.choice(cards)