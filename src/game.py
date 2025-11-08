from collections import deque
from src.deck import create_deck, deal_cards

# Constants
MAX_ROUNDS = 3000  # Prevent infinite games
WAR_CARDS_FACEDOWN = 3  # Standard war rules


def play_round(p1_hand, p2_hand, stats):
    """
    Play a single round of War.
    
    Args:
        p1_hand: deque of player 1's cards
        p2_hand: deque of player 2's cards
        stats: dictionary tracking game statistics
    
    Returns:
        bool: True if game should continue, False if game is over
    """
    # Check if either player is out of cards
    if not p1_hand:
        stats['winner'] = 2
        return False
    if not p2_hand:
        stats['winner'] = 1
        return False
    
    # Draw top cards
    p1_card = p1_hand.popleft()
    p2_card = p2_hand.popleft()
    
    # Cards in play for this round
    cards_in_play = [p1_card, p2_card]
    
    # Compare cards
    if p1_card > p2_card:
        # Player 1 wins
        p1_hand.extend(cards_in_play)
    elif p2_card > p1_card:
        # Player 2 wins
        p2_hand.extend(cards_in_play)
    else:
        # War!
        stats['wars'] += 1
        war_result = handle_war(p1_hand, p2_hand, cards_in_play, stats)
        if not war_result:
            return False  # Game ended during war
    
    stats['rounds'] += 1
        
    # Check for max rounds (potential infinite game)
    if stats['rounds'] >= MAX_ROUNDS:
        stats['hit_max_rounds'] = True
        stats['winner'] = None
        return False
    
    return True


def handle_war(p1_hand, p2_hand, cards_in_play, stats, war_depth=0):
    """
    Handle a war scenario when cards tie.
    
    Args:
        p1_hand: deque of player 1's cards
        p2_hand: deque of player 2's cards
        cards_in_play: list of cards currently in the pot
        stats: dictionary tracking game statistics
        war_depth: recursion depth for tracking double/triple wars
    
    Returns:
        bool: True if war completed successfully, False if game ended
    """
    # Track war depth for statistics
    if war_depth > 0:
        stats['double_wars'] += 1
    
    # Each player needs 4 cards total (3 facedown + 1 faceup)
    cards_needed = WAR_CARDS_FACEDOWN + 1
    
    # Check if players have enough cards
    if len(p1_hand) < cards_needed:
        # Player 1 doesn't have enough cards, player 2 wins
        stats['winner'] = 2
        return False
    if len(p2_hand) < cards_needed:
        # Player 2 doesn't have enough cards, player 1 wins
        stats['winner'] = 1
        return False
    
    # Place cards facedown
    for _ in range(WAR_CARDS_FACEDOWN):
        cards_in_play.append(p1_hand.popleft())
        cards_in_play.append(p2_hand.popleft())
    
    # Draw faceup cards
    p1_card = p1_hand.popleft()
    p2_card = p2_hand.popleft()
    cards_in_play.extend([p1_card, p2_card])
    
    # Compare faceup cards
    if p1_card > p2_card:
        # Player 1 wins the war
        p1_hand.extend(cards_in_play)
        return True
    elif p2_card > p1_card:
        # Player 2 wins the war
        p2_hand.extend(cards_in_play)
        return True
    else:
        # Another war! (recursive)
        stats['wars'] += 1
        return handle_war(p1_hand, p2_hand, cards_in_play, stats, war_depth + 1)


def play_game():
    """
    Play a complete game of War and return statistics.
    
    Returns:
        dict: Statistics from the game including:
            - rounds: total number of rounds
            - wars: number of wars
            - double_wars: number of wars during wars
            - winner: 1, 2, or None (if hit max rounds)
            - hit_max_rounds: bool indicating if game hit the limit
            - p1_stack_sizes: list of player 1's stack size after each round
            - p2_stack_sizes: list of player 2's stack size after each round
    """
    # Initialize game
    deck = create_deck()
    p1_hand, p2_hand = deal_cards(deck)
    
    # Initialize statistics
    stats = {
        'rounds': 0,
        'wars': 0,
        'double_wars': 0,
        'winner': None,
        'hit_max_rounds': False
    }
    
    # Play until game ends
    while play_round(p1_hand, p2_hand, stats):
        pass
    
    return stats