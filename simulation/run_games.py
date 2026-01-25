from simulation.boerenbridge_game import BoerenbridgeGame
from data.data_logger import DataLogger

NUM_GAMES = 100_000
TOTAL_ROUNDS = 16
NUM_PLAYERS = 4

round_logger = DataLogger("data/round_log.csv")
trick_logger = DataLogger("data/trick_log.csv")

def log_trick(event, engine):
    trick = event["trick"]
    
    trick_logger.log({
        "game_id": current_game,
        "round_number": engine.round_number,
        "trick_number": event["trick_number"],
        "starter": event["starter"],
        "winner": event["winner"],
        "trump_suit": event["trump"],

        "card_p0": trick[0],
        "card_p1": trick[1],
        "card_p2": trick[2],
        "card_p3": trick[3],
    })

def log_round(engine):
    round_logger.log({
        "game_id": current_game,
        "round_number": engine.round_number,
        "cards_per_player": engine.cards_per_player,
        "starting_player": (engine.round_number - 1) % engine.NUM_PLAYERS,
        "trump_suit": engine.trump_suit,
        
        "bet_p0": engine.bets[0],
        "bet_p1": engine.bets[1],
        "bet_p2": engine.bets[2],
        "bet_p3": engine.bets[3],

        "tricks_p0": engine.tricks_won[0],
        "tricks_p1": engine.tricks_won[1],
        "tricks_p2": engine.tricks_won[2],
        "tricks_p3": engine.tricks_won[3],
        
        "points_p0": engine.round_points[0],
        "points_p1": engine.round_points[1],
        "points_p2": engine.round_points[2],
        "points_p3": engine.round_points[3],
    }) 

highest_score = -1
lowest_score = int(1000)

for current_game in range(NUM_GAMES):
    game = BoerenbridgeGame(
        seed=current_game,
        on_trick_end=log_trick,
        on_round_end=log_round
    )
    scores = game.play_game()

    for score in scores:
        if score > highest_score:
            highest_score = score
        if score < lowest_score:
            lowest_score = score

    if current_game % 1000 == 0:
        print(f"Finished game {current_game}")

print("Highest score:", highest_score)
print("Lowest score:", lowest_score)

#     for i in range(NUM_PLAYERS):
#         total_scores[i] += scores[i]
#         for j in range(TOTAL_ROUNDS):
#             total_bets[i][j] += bets[i][j]
            
# for i in range(NUM_PLAYERS):
#     for j in range(TOTAL_ROUNDS):
#         total_bets[i][j] /= NUM_GAMES

# print("Average total scores: ", total_scores)

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
