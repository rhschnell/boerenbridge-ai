import random
from engine.card import Card

class BoerenbridgeEngine:
    NUM_PLAYERS = 4
    NO_TRUMP = 4

    # Initializer for BoerenbridgeEngine
    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

        # Round state (initialized in reset_round)
        self.deck = None

        # Contains the hands of the players
        self.hands = None

        # Contains the cards played in the current trick
        self.current_trick = None

        # Keeps track of which trick number were in during the roudn
        self.trick_number = None

        # Keeps track who starts the next trick
        self.trick_starter = None

        # Player whos turn it currently is
        self.current_player = None
        
        # Amount of cards per player, differs from the round number
        self.cards_per_player = None
        self.round_number = None

        # Bets placed, tricks won and the final scores after the round
        self.bets = None
        self.tricks_won = None

        # Contains the amount of points after the round
        self.round_points = None

        self.trump_suit = None
        self.round_over = False
        self.phase = None  
    
    # Resets the round, takes the new round number as a parameter
    def reset_round(self, round_number) -> None:
        assert round_number in range(1, 17)
        
        self.round_number = round_number
        self.cards_per_player = round_number if round_number <= 8 else 17 - round_number

        assert self.cards_per_player > 0
        assert self.cards_per_player <= 8

        self.trick_starter = (round_number - 1) % self.NUM_PLAYERS
        self.current_player = self.trick_starter
        
        cycle = (round_number - 1) % 5
        self.trump_suit = self.NO_TRUMP if cycle == 4 else cycle

        self.deck = self._create_deck()
        
        assert len(self.deck) == 32

        self.rng.shuffle(self.deck)
        self.hands = self._deal_cards(self.cards_per_player)
        
        for hand in self.hands:
            assert len(hand) == self.cards_per_player
        assert len(self.deck) == 32 - self.cards_per_player * self.NUM_PLAYERS

        self.current_trick = [None] * self.NUM_PLAYERS
        self.trick_number = 0
        self.bets = [None] * self.NUM_PLAYERS
        self.tricks_won = [0] * self.NUM_PLAYERS
        self.round_points = [0] * self.NUM_PLAYERS

        self.round_over = False
        self.phase = "betting"
  
    # Method which makes the bet for the player
    # Checks if the player hasn't already bet and if so, places the bet
    def make_bet(self, player_id, bet_amount):
        assert not self.round_over
        assert self.bets[player_id] is None
        assert 0 <= bet_amount <= self.cards_per_player

        if not (0 <= bet_amount <= self.cards_per_player):
            raise ValueError("Illegal bet amount")
        
        if self.bets[player_id] is not None:
            raise ValueError("Player already bet")
        
        if all(b is not None for i, b in enumerate(self.bets) if i != player_id):
            if sum(b for b in self.bets if b is not None) + bet_amount == self.cards_per_player:
                raise ValueError("Last player cannot make total bets equal cards")
                    
        self.bets[player_id] = bet_amount

    # Checks if all player have made a bet
    def all_bets_made(self):
        assert len(self.bets) == self.NUM_PLAYERS
        return all(b is not None for b in self.bets)
    
    # This method returns all the cards a player is allowed to play during a trick
    # keeping in mind trump suits and the leading suit
    def legal_actions(self, player_id):
        hand = self.hands[player_id]

        assert len(hand) == self.cards_per_player - self.trick_number
        assert self.current_trick[player_id] is None
        assert len(hand) > 0

        # If player is starting the trick
        if self.current_trick[self.trick_starter] is None:
            return hand.copy()

        lead_suit = self.current_trick[self.trick_starter].suit

        follow = [card for card in hand if card.suit == lead_suit]
        
        if follow:
            return follow
        
        return hand.copy()
    
    # Plays the card for a player by removing the card from their hand an placing it in the trick
    def play_card(self, player_id, card):
        assert not self.round_over
        assert player_id == self.current_player
        assert self.current_trick[player_id] is None
        assert card in self.legal_actions(player_id)

        self.hands[player_id].remove(card)
        self.current_trick[player_id] = card

        self.current_player = (self.current_player + 1) % self.NUM_PLAYERS    
        
        assert card not in self.hands[player_id]
        assert self.current_trick[player_id] == card

        if all(value is not None for value in self.current_trick):
            return self._resolve_trick()    
        return None
    
    # Returns true if the round is over
    def is_round_over(self):
        return self.round_over

    # Resolves the trick, updating values such as who is able to start the next trick
    def _resolve_trick(self):
        assert all(card is not None for card in self.current_trick)
        completed_trick = self.current_trick.copy()
        starter = self.trick_starter
        trump = self.trump_suit

        winner = self._determine_trick_winner()
        
        self.tricks_won[winner] += 1
        self.trick_number += 1
        
        assert self.trick_number <= self.cards_per_player

        # If this was the last trick, compute final score for the round
        if self.trick_number == self.cards_per_player:
            self._resolve_final_score()
        
        self.current_player = winner
        self.trick_starter = winner
        self.current_trick = [None] * self.NUM_PLAYERS
        
        return {
            "trick": completed_trick,
            "starter": starter,
            "winner": winner,
            "trump": trump,
            "trick_number": self.trick_number
        }
    
    # Calculates the winner of the trick
    def _determine_trick_winner(self):
        leading_suit = self.current_trick[self.current_player].suit
        
        assert self.current_trick[self.trick_starter] is not None
        
        best_player = self.current_player

        # 100 is added to the rank of the card if the suit is the trump suit
        best_strength = self._card_strength(self.current_trick[best_player], leading_suit)

        for p, card in enumerate(self.current_trick):
            strength = self._card_strength(card, leading_suit)
            if strength > best_strength:
                best_player = p
                best_strength = strength

        return best_player
    
    def _resolve_final_score(self):
        for i in range(self.NUM_PLAYERS):
            if (self.tricks_won[i] == self.bets[i]):
                self.round_points[i] = 10 + self.tricks_won[i]
            else:
                self.round_points[i] = self.tricks_won[i] - self.bets[i]

        self.round_over = True

    def _create_deck(self):
        return [
            Card(suit, rank)
            for suit in range(4)
            for rank in range(0, 8)
        ]

    def _deal_cards(self, cards_per_player):
        hands = [[] for _ in range(self.NUM_PLAYERS)]

        for _ in range (cards_per_player):
            for p in range(self.NUM_PLAYERS):
                hands[p].append(self.deck.pop())

        return hands

    def _card_strength(self, card, leading_suit):
        if self.trump_suit != self.NO_TRUMP and card.suit == self.trump_suit:
            return 100 + card.rank
        if leading_suit == None:
            return card.rank
        if card.suit == leading_suit:
            return card.rank
        return 0
    