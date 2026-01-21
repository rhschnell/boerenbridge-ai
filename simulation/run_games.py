from simulation.boerenbridge_game import BoerenbridgeGame

NUM_GAMES = 1
TOTAL_ROUNDS = 16
NUM_PLAYERS = 4

total_scores = [0] * NUM_PLAYERS
total_bets = [[0] * TOTAL_ROUNDS for _ in range (NUM_PLAYERS)]

for seed in range(NUM_GAMES):
    game = BoerenbridgeGame(seed=seed)
    scores, bets = game.play_game()

    for i in range(NUM_PLAYERS):
        total_scores[i] += scores[i]
        for j in range(TOTAL_ROUNDS):
            total_bets[i][j] += bets[i][j]
            
for i in range(NUM_PLAYERS):
    for j in range(TOTAL_ROUNDS):
        total_bets[i][j] /= NUM_GAMES

print("Average total scores: ", total_scores)

# def run_games(num_games):
#     game = BoerenbridgeGame(seed=0)
    
#     TOTAL_ROUNDS = game.TOTAL_ROUNDS
#     NUM_PLAYERS = game.NUM_PLAYERS

#     total_scores = [0] * NUM_PLAYERS
#     total_bets = [[0] * TOTAL_ROUNDS for _ in range (NUM_PLAYERS)]

#     for seed in range(num_games):
#         game = BoerenbridgeGame(seed=seed)
#         scores, bets = game.play_game()

#         for i in range(NUM_PLAYERS):
#             total_scores[i] += scores[i]

#         for i in range(game.NUM_PLAYERS):
#             for j in range(game.TOTAL_ROUNDS):
#                 total_bets[i][j] += bets[i][j]
                
#     for i in range(game.NUM_PLAYERS):
#         for j in range(game.TOTAL_ROUNDS):
#             total_bets[i][j] /= num_games

# if __name__ == "__main__":
#     run_games(NUM_GAMES)
#     print("FINISHED")
