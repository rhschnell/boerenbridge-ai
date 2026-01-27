BOT_VERSION = "heuristic_v1"

class HeuristicBot:
    CARD_EV_NT = [0, 0.03, 0.06, 0.1, 0.13, 0.16, 0.19, 0.23]
    CARD_EV_T = [0.77, 0.81, 0.84, 0.87, 0.9, 0.94, 0.97, 1]
    CARD_EV_SANS = [0, 0.02, 0.04, 0.1, 0.2, 0.4, 0.8, 1]
    
    def __init__(self, player_id):
        self.player_id = player_id

    def make_bet(self, engine):
        hand = engine.hands[self.player_id]
        trump = engine.trump_suit
        return round(self.compute_expected_tricks(hand, trump))
    
    def play_card(self, engine):
        cards = engine.legal_actions(self.player_id)
        
        tricks_won = engine.tricks_won[self.player_id]
        bet = engine.bets[self.player_id]
        need = bet - tricks_won
                
        lead_player = engine.trick_starter
        lead_card = engine.current_trick[lead_player]
        remaining_tricks = engine.cards_per_player - engine.trick_number

        want_to_win = False
        if need == 0:
            want_to_win = False
        if need >= remaining_tricks: 
            want_to_win = True

        if lead_card is None:
            if want_to_win:
                card, _ = self.find_strongest_card(engine, cards, None)
                return card
            else:
                card, _ = self.find_weakest_card(engine, cards, None)
                return card
            
        lead_suit = lead_card.suit

        if want_to_win:
            return self.lowest_winning_card(engine, cards, lead_suit)
        else:
            losing = self.highest_losing_card(engine, cards, lead_suit)
            if losing is not None:
                return losing
            card, _ = self.find_weakest_card(engine, cards, lead_suit)
            return card

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

    def find_strongest_card(self, engine, cards, lead_suit):
        best_card = None
        best_strength = -1

        for card in cards:
            strength = engine._card_strength(card, lead_suit)
            if strength > best_strength:
                best_strength = strength
                best_card = card

        return best_card, best_strength
    
    def find_weakest_card(self, engine, cards, lead_suit):
        weakest_card = None
        weakest_strength = float("inf")

        for card in cards:
            strength = engine._card_strength(card, lead_suit)
            if strength < weakest_strength:
                weakest_strength = strength
                weakest_card = card

        return weakest_card, weakest_strength
    
    def lowest_winning_card(self, engine, cards, lead_suit):
        best_strength_in_trick = -1

        for card in engine.current_trick:
            if card is None:
                continue
            strength = engine._card_strength(card, lead_suit)
            if strength > best_strength_in_trick:
                best_strength_in_trick = strength

        chosen = None
        chosen_strength = float("inf")

        for card in cards:
            strength = engine._card_strength(card, lead_suit)
            if strength > best_strength_in_trick and strength < chosen_strength:
                chosen = card
                chosen_strength = strength

        if chosen is None:
            weakest, _ = self.find_weakest_card(engine, cards, lead_suit)
            chosen = weakest
        return chosen
    
    def highest_losing_card(self, engine, cards, lead_suit):
        losing_card = None
        losing_strength = -1

        for card in cards:
            strength = engine._card_strength(card, lead_suit)
            if strength == 0 and strength > losing_strength:
                losing_card = card
                losing_strength = strength

        return losing_card
    