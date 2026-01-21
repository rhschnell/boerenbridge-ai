from simulation.boerenbridge_game import BoerenbridgeGame

if __name__ == "__main__":
    game = BoerenbridgeGame(seed=0)
    scores, bets = game.play_game()

    print("Final scores:", scores)
