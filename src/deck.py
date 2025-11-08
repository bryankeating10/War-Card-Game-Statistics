# src/deck.py
import random
from collections import deque

# Constants
CARD_RANKS = list(range(2, 15))  # 2-14 (J=11, Q=12, K=13, A=14)
NUM_SUITS = 4

def create_deck():
    """
    Creates a standard 52-card deck.
    Returns a list of integers where suits don't matter, just rank.
    """
    deck = []
    for rank in CARD_RANKS:
        for _ in range(NUM_SUITS):
            deck.append(rank)
    return deck

def deal_cards(deck):
    """
    Shuffles deck and deals 26 cards to each player.
    Returns two deques (for efficient pop/append operations).
    """
    shuffled = deck.copy()
    random.shuffle(shuffled)
    
    p1_hand = deque(shuffled[:26])
    p2_hand = deque(shuffled[26:])
    
    return p1_hand, p2_hand