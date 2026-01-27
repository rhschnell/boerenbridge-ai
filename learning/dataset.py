import pandas as pd
import numpy as np

NUM_SUITS = 4
NUM_RANKS = 8
NUM_CARDS = NUM_SUITS * NUM_RANKS

EXTRA_FEATURES = 6
FEATURE_DIM = NUM_CARDS + EXTRA_FEATURES

OBJECTIVE_MAP = {
    "must_win": 2, 
    "can_win": 1,
    "must_lose": 0
}

def parse_card(card):
    if len(card) == 1:
        # suit must be 0, rank is the digit
        return 0, int(card)
    
    return int(card[0]), int(card[1:])

def card_id(suit, rank):
    return suit * NUM_RANKS + rank

def feature_row(row):
    features = []

    hand_vec = np.zeros(NUM_CARDS, dtype=np.int8)

    for c in row['legal_cards'].split("|"):
        s, r = parse_card(c)
        hand_vec[card_id(s, r)] = 1
    
    features.extend(hand_vec)
    
    features.extend([
        row['round_number'],
        row['trick_number'],
        row['trump_suit'],
        row['bet'],
        row['tricks_won'],
        OBJECTIVE_MAP[row['objective']]    
    ])
    cs, cr = parse_card(row['chosen_card'])

    target = card_id(cs, cr)

    return features, target

def load_dataset(path="data/decision_log.csv"):    
    decisions = pd.read_csv(path)

    N = len(decisions)
    print(f"Dataset size: {N}")

    X = np.zeros((N, FEATURE_DIM), dtype=np.int8)
    Y = np.zeros(N, dtype=np.int16)

    for i, row in enumerate(decisions.itertuples(index=False)):
        hand_vec = np.zeros(NUM_CARDS, dtype=np.int8)
        
        for c in row.legal_cards.split("|"):
            s, r = map(int, c.split(","))
            hand_vec[card_id(s, r)] = 1

        X[i, :NUM_CARDS] = hand_vec
        
        X[i, NUM_CARDS:] = [
            row.round_number,
            row.trick_number,
            row.trump_suit,
            row.bet,
            row.tricks_won,
            OBJECTIVE_MAP[row.objective]
        ]

        Y[i] = card_id(row.chosen_suit, row.chosen_rank)

        if i % 100000  == 0:
            print(f"Finished row {i}")
            

    return X, Y
