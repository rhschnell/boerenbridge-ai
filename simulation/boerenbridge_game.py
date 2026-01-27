import random
from engine.game_engine import BoerenbridgeEngine

class BoerenbridgeGame:
    TOTAL_ROUNDS = 16
    NUM_PLAYERS = 4

    def __init__(self, bots=None, seed=None, on_trick_end=None, on_round_end=None):
        self.engine = BoerenbridgeEngine(seed=seed)
        self.rng = random.Random(seed)
        self.cumulative_scores = [0] * self.NUM_PLAYERS
        self.bets_made = [0] * self.NUM_PLAYERS

        self.bots = bots
        self.on_trick_end = on_trick_end
        self.on_round_end = on_round_end

        self.total_scores = [0] * self.NUM_PLAYERS

    def play_game(self):
        for round_number in range(1, self.TOTAL_ROUNDS + 1):
            self.play_round(round_number)

        return self.total_scores

    def play_round(self, round_number):
        self.engine.reset_round(round_number)

        starting_player = self.engine.trick_starter
        total_bets = 0

        for i in range(self.NUM_PLAYERS):
            player_id = (starting_player + i) % self.NUM_PLAYERS
            bet = self.bots[player_id].make_bet(self.engine)

            # Last person to bet
            if i == self.NUM_PLAYERS - 1:
                if total_bets + bet == self.engine.cards_per_player:
                    bet = (bet + 1) % (self.engine.cards_per_player + 1)

            self.engine.make_bet(player_id, bet)
            total_bets += bet

        while not self.engine.is_round_over():
            player_id = self.engine.current_player
            card = self.bots[player_id].play_card(self.engine)
            result = self.engine.play_card(player_id, card)

            if result is not None and self.on_trick_end:
                self.on_trick_end(result, self.engine)

        for i in range(self.NUM_PLAYERS):
            self.total_scores[i] += self.engine.round_points[i]

        if self.on_round_end:
            self.on_round_end(self.engine)
                
    # def play_round(self, round_number):
    #     self.engine.reset_round(round_number)

    #     filename = f"_heuristic_bot/round_{round_number}.txt"
    #     with open(filename, "w") as f:
    #         f.write(f"Round {round_number}\n")
    #         f.write(f"Cards per player: {self.engine.cards_per_player}\n")
    #         f.write(f"Trump suit index: {self.engine.trump_suit}\n")
    #         f.write("-" * 40 + "\n\n")

    #         starting_player = self.engine.trick_starter
    #         total_bets = 0

    #         for i in range(self.NUM_PLAYERS):
    #             player_id = (starting_player + i) % self.NUM_PLAYERS
    #             bet = self.bots[player_id].make_bet(self.engine)

    #             if i == self.NUM_PLAYERS - 1:
    #                 if total_bets + bet == self.engine.cards_per_player:
    #                     bet = (bet + 1) % (self.engine.cards_per_player + 1)

    #             self.engine.make_bet(player_id, bet)
    #             total_bets += bet
    #             self.cumulative_bets[i][round_number - 1] += bet

    #         f.write(
    #             f"Player 0: {self.engine.hands[0]}\n" 
    #             f"Player 1: {self.engine.hands[1]}\n" 
    #             f"Player 2: {self.engine.hands[2]}\n" 
    #             f"Player 3: {self.engine.hands[3]}\n\n" 
    #         )

    #         while not self.engine.is_round_over():
    #             player_id = self.engine.current_player
    #             card = self.bots[player_id].play_card(self.engine)
    #             result = self.engine.play_card(player_id, card)


    #             if result is not None:
    #                 f.write(
    #                     f"Trick {result['trick_number']} "
    #                     f"(starter: Player {result['starter']}, "
    #                     f"winner: Player {result['winner']}, "
    #                     f"trump: {result['trump']})\n"
    #                 )
    #                 f.write(str(result["trick"]) + "\n\n")

    #         for i in range(self.NUM_PLAYERS):
    #             self.total_scores[i] += self.engine.round_points[i]
                
    #         f.write("Bets: " + str(self.engine.bets) + "\n")
    #         f.write("Tricks won: " + str(self.engine.tricks_won) + "\n")
    #         f.write("Round points: " + str(self.engine.round_points) + "\n")
    #         f.write("Total scores: " + str(self.total_scores) + "\n")   

