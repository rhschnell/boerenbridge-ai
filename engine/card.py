from dataclasses import dataclass

@dataclass(frozen=False)
class Card:
    # SUIT_NAMES = ["♠", "♥", "♦", "♣"]
    # RANK_NAMES = {11: "J", 12: "Q", 13: "K", 14: "A"}

    def __init__(self, suit: int, rank: int):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        # rank_str = self.RANK_NAMES.get(self.rank, str(self.rank))
        # suit_str = self.SUIT_NAMES[self.suit]
        return f"{self.suit}{self.rank}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    