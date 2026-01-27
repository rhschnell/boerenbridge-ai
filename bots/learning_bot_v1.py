import joblib
import numpy as np
from engine.card import Card

BOT_VERSION = "learning_v1"
MODEL_PATH = "learning/models/card_policy_500iter_v1.pkl"
NUM_SUITS = 4
NUM_RANKS = 8
NUM_CARDS = 32

OBJECTIVE_MAP = {
    "must_win": 2,
    "can_win": 1,
    "must_lose": 0
}

class LearningBotV1:
    CARD_EV_NT = [0, 0.03, 0.06, 0.1, 0.13, 0.16, 0.19, 0.23]
    CARD_EV_T = [0.77, 0.81, 0.84, 0.87, 0.9, 0.94, 0.97, 1]
    CARD_EV_SANS = [0, 0.02, 0.04, 0.1, 0.2, 0.4, 0.8, 1]

    def __init__(self, player_id, logger=None):
        self.player_id = player_id
        self.logger = logger
        self.model = joblib.load(MODEL_PATH)

    def make_bet(self, engine):
        hand = engine.hands[self.player_id]
        trump = engine.trump_suit
        return round(self.compute_expected_tricks(hand, trump))
    
    def compute_expected_tricks(self, hand, trump):
        result = 0

        for card in hand:
            if trump == 4:
                result += self.CARD_EV_SANS[card.rank]
            elif card.suit == trump:
                result += self.CARD_EV_T[card.rank]
            else: 
                result += self.CARD_EV_NT[card.rank]

        return result
    
    def play_card(self, engine):
        cards = engine.legal_actions(self.player_id)

        X = self.build_feature_vector(engine, cards)
        probs = self.model.predict_proba(X)[0]

        ranked_ids = np.argsort(probs)[::-1]
        
        for card_id in ranked_ids:
            for card in cards:
                if self.card_to_id(card) == card_id:
                    return card
                
        return cards[0]
    
    def card_to_id(self, card):
        return card.suit * 8 + card.rank
    
    def build_feature_vector(self, engine, cards):
        x = np.zeros(NUM_CARDS + 6, dtype=np.float32)

        for c in cards:
            x[self.card_to_id(c)] = 1
        
        offset = NUM_CARDS

        x[offset + 0] = engine.round_number
        x[offset + 1] = engine.trick_number
        x[offset + 2] = engine.trump_suit
        x[offset + 3] = engine.bets[self.player_id]
        x[offset + 4] = engine.tricks_won[self.player_id]
        x[offset + 5] = OBJECTIVE_MAP[self.compute_play_objective(engine)]

        return x.reshape(1, -1)
        
    def compute_play_objective(self, engine):
        bet = engine.bets[self.player_id]
        tricks_won = engine.tricks_won[self.player_id]
        remaining_tricks = engine.cards_per_player - engine.trick_number

        need = bet - tricks_won

        if need == 0:
            return "must_lose"
        if need >= remaining_tricks:
            return "must_win"
        return "can_win"


    def card_to_id(self, card):
        return card.suit * 8 + card.rank
    
    def build_feature_vector(self, engine, cards):
        x = np.zeros(NUM_CARDS + 6, dtype=np.float32)

        for c in cards:
            x[self.card_to_id(c)] = 1
        
        offset = NUM_CARDS

        x[offset + 0] = engine.round_number
        x[offset + 1] = engine.trick_number
        x[offset + 2] = engine.trump_suit
        x[offset + 3] = engine.bets[self.player_id]
        x[offset + 4] = engine.tricks_won[self.player_id]
        x[offset + 5] = OBJECTIVE_MAP[self.compute_play_objective(engine)]

        return x.reshape(1, -1)
        
    def compute_play_objective(self, engine):
        bet = engine.bets[self.player_id]
        tricks_won = engine.tricks_won[self.player_id]
        remaining_tricks = engine.cards_per_player - engine.trick_number

        need = bet - tricks_won

        if need == 0:
            return "must_lose"
        if need >= remaining_tricks:
            return "must_win"
        return "can_win"

    def log_decision(self, engine, legal_cards, chosen_card, logger):
        row = {
            "bot_version": BOT_VERSION,
            "player_id": self.player_id,
            "round_number": engine.round_number,
            "trick_number": engine.trick_number,
            "trump_suit": engine.trump_suit,
            "objective": self.compute_play_objective(engine),
            "bet": engine.bets[self.player_id],
            "tricks_won": engine.tricks_won[self.player_id],
            "chosen_suit": chosen_card.suit,
            "chosen_rank": chosen_card.rank,
            "legal_cards": "|".join(f"{c.suit},{c.rank}" for c in legal_cards),
        }
        logger.log(row)


# BOT_VERSION = "learning_v1"
# MODEL_PATH = "learning/models/card_policy_500iter_v1.pl=kl"
# NUM_SUITS = 4
# NUM_RANKS = 8
# NUM_CARDS = 32

# OBJECTIVE_MAP = {
#     "must_win": 2,
#     "can_win": 1,
#     "must_lose": 0
# }

# class LearningBotV1:
#     CARD_EV_NT = [0, 0.03, 0.06, 0.1, 0.13, 0.16, 0.19, 0.23]
#     CARD_EV_T = [0.77, 0.81, 0.84, 0.87, 0.9, 0.94, 0.97, 1]
#     CARD_EV_SANS = [0, 0.02, 0.04, 0.1, 0.2, 0.4, 0.8, 1]
    
#     def __init__(self, player_id, logger=None):
#         self.player_id = player_id
#         self.logger = logger

#     def make_bet(self, engine):
#         hand = engine.hands[self.player_id]
#         trump = engine.trump_suit
#         return round(self.compute_expected_tricks(hand, trump))
    
#     def play_card(self, engine):
#         cards = engine.legal_actions(self.player_id)
#         objective = self.compute_play_objective(engine)

#         lead_player = engine.trick_starter
#         lead_card = engine.current_trick[lead_player]

#         if lead_card is None:
#             chosen = self._lead_card(engine, cards, objective)
#         else:
#             lead_suit = lead_card.suit

#             if objective in ("must_win", "can_win"):
#                 chosen = self.lowest_winning_card(engine, cards, lead_suit)
#             else:
#                 chosen = None

#             if chosen is None:
#                 losing = self.highest_losing_card(engine, cards, None)
#                 if losing:
#                     chosen = losing
#                 else:
#                     chosen, _ = self.find_weakest_card(engine, cards, None)

#         if self.logger is not None:
#             self.log_decision(engine, cards, chosen, self.logger)

#         return chosen
    
#     def compute_play_objective(self, engine):
#         bet = engine.bets[self.player_id]
#         tricks_won = engine.tricks_won[self.player_id]
#         remaining_tricks = engine.cards_per_player - engine.trick_number

#         need = bet - tricks_won

#         if need == 0:
#             return "must_lose"
#         if need >= remaining_tricks:
#             return "must_win"
#         return "can_win"

#     def compute_expected_tricks(self, hand, trump):
#         result = 0

#         for card in hand:
#             if trump == 4:
#                 result += self.CARD_EV_SANS[card.rank]
#             elif card.suit == trump:
#                 result += self.CARD_EV_T[card.rank]
#             else: 
#                 result += self.CARD_EV_NT[card.rank]

#         return result

#     def find_strongest_card(self, engine, cards, lead_suit):
#         best_card = None
#         best_strength = -1

#         for card in cards:
#             strength = engine._card_strength(card, lead_suit)
#             if strength > best_strength:
#                 best_strength = strength
#                 best_card = card

#         return best_card, best_strength
    
#     def find_weakest_card(self, engine, cards, lead_suit):
#         weakest_card = None
#         weakest_strength = float("inf")

#         for card in cards:
#             strength = engine._card_strength(card, lead_suit)
#             if strength < weakest_strength:
#                 weakest_strength = strength
#                 weakest_card = card

#         return weakest_card, weakest_strength
    
#     def lowest_winning_card(self, engine, cards, lead_suit):
#         best_strength_in_trick = -1

#         for card in engine.current_trick:
#             if card is None:
#                 continue
#             strength = engine._card_strength(card, lead_suit)
#             if strength > best_strength_in_trick:
#                 best_strength_in_trick = strength

#         chosen = None
#         chosen_strength = float("inf")

#         for card in cards:
#             strength = engine._card_strength(card, lead_suit)
#             if strength > best_strength_in_trick and strength < chosen_strength:
#                 chosen = card
#                 chosen_strength = strength

#         if chosen is None:
#             weakest, _ = self.find_weakest_card(engine, cards, lead_suit)
#             chosen = weakest
#         return chosen
    
#     def highest_losing_card(self, engine, cards, lead_suit):
#         losing_card = None
#         losing_strength = -1

#         for card in cards:
#             strength = engine._card_strength(card, lead_suit)
#             if strength == 0 and strength > losing_strength:
#                 losing_card = card
#                 losing_strength = strength

#         return losing_card
    
#     def _lead_card(self, engine, cards, objective):
#         if objective in ("must_win", "can_win"):
#             card, _ = self.find_strongest_card(engine, cards, None)
#             return card
#         else:
#             card, _ = self.find_weakest_card(engine, cards, None)
#             return card
        
#     def log_decision(self, engine, legal_cards, chosen_card, logger):
#         row = {
#             "bot_version": BOT_VERSION,
#             "player_id": self.player_id,
#             "round_number": engine.round_number,
#             "trick_number": engine.trick_number,
#             "trump_suit": engine.trump_suit,
#             "objective": self.compute_play_objective(engine),
#             "bet": engine.bets[self.player_id],
#             "tricks_won": engine.tricks_won[self.player_id],
#             "chosen_suit": chosen_card.suit,
#             "chosen_rank": chosen_card.rank,
#             "legal_cards": "|".join(f"{c.suit},{c.rank}" for c in legal_cards),
#         }
#         logger.log(row)
