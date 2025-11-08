import pytest
from collections import deque
from game import play_round, handle_war, play_game, MAX_ROUNDS


def test_play_round_p1_wins():
    """Player 1 should win when their card is higher"""
    p1_hand = deque([10, 5])
    p2_hand = deque([3, 8])
    stats = {'rounds': 0, 'wars': 0, 'double_wars': 0, 'p1_stack_sizes': [], 'p2_stack_sizes': []}
    
    result = play_round(p1_hand, p2_hand, stats)
    
    assert result is True  # Game continues
    assert len(p1_hand) == 3  # Won 2 cards (10, 3), has 1 remaining (5)
    assert len(p2_hand) == 1  # Lost a card
    assert stats['rounds'] == 1


def test_play_round_p2_wins():
    """Player 2 should win when their card is higher"""
    p1_hand = deque([3, 5])
    p2_hand = deque([10, 8])
    stats = {'rounds': 0, 'wars': 0, 'double_wars': 0, 'p1_stack_sizes': [], 'p2_stack_sizes': []}
    
    result = play_round(p1_hand, p2_hand, stats)
    
    assert result is True
    assert len(p1_hand) == 1
    assert len(p2_hand) == 3


def test_play_round_triggers_war():
    """Equal cards should trigger a war"""
    p1_hand = deque([7, 2, 3, 4, 5, 10])
    p2_hand = deque([7, 6, 7, 8, 9, 2])
    stats = {'rounds': 0, 'wars': 0, 'double_wars': 0, 'p1_stack_sizes': [], 'p2_stack_sizes': []}
    
    result = play_round(p1_hand, p2_hand, stats)
    
    assert result is True
    assert stats['wars'] == 1


def test_play_round_game_ends_p1_empty():
    """Game should end when player 1 runs out of cards"""
    p1_hand = deque([])
    p2_hand = deque([5, 6, 7])
    stats = {'rounds': 0, 'wars': 0, 'double_wars': 0, 'winner': None, 'p1_stack_sizes': [], 'p2_stack_sizes': []}
    
    result = play_round(p1_hand, p2_hand, stats)
    
    assert result is False
    assert stats['winner'] == 2


def test_play_round_game_ends_p2_empty():
    """Game should end when player 2 runs out of cards"""
    p1_hand = deque([5, 6, 7])
    p2_hand = deque([])
    stats = {'rounds': 0, 'wars': 0, 'double_wars': 0, 'winner': None, 'p1_stack_sizes': [], 'p2_stack_sizes': []}
    
    result = play_round(p1_hand, p2_hand, stats)
    
    assert result is False
    assert stats['winner'] == 1


def test_handle_war_p1_wins():
    """Player 1 should win war with higher face-up card"""
    p1_hand = deque([1, 2, 3, 10])  # 10 is the face-up card
    p2_hand = deque([4, 5, 6, 7])   # 7 is the face-up card
    cards_in_play = [8, 8]  # The tied cards
    stats = {'wars': 0, 'double_wars': 0, 'winner': None}
    
    result = handle_war(p1_hand, p2_hand, cards_in_play, stats)
    
    assert result is True
    assert len(p1_hand) == 10  # Won all 10 cards (2 tied + 8 from war)
    assert len(p2_hand) == 0


def test_handle_war_p2_wins():
    """Player 2 should win war with higher face-up card"""
    p1_hand = deque([1, 2, 3, 5])
    p2_hand = deque([4, 5, 6, 14])  # Ace wins
    cards_in_play = [7, 7]
    stats = {'wars': 0, 'double_wars': 0, 'winner': None}
    
    result = handle_war(p1_hand, p2_hand, cards_in_play, stats)
    
    assert result is True
    assert len(p1_hand) == 0
    assert len(p2_hand) == 10


def test_handle_war_insufficient_cards_p1():
    """Player 1 loses if they don't have enough cards for war"""
    p1_hand = deque([1, 2])  # Only 2 cards, needs 4
    p2_hand = deque([4, 5, 6, 7, 8])
    cards_in_play = [9, 9]
    stats = {'wars': 0, 'double_wars': 0, 'winner': None}
    
    result = handle_war(p1_hand, p2_hand, cards_in_play, stats)
    
    assert result is False
    assert stats['winner'] == 2


def test_handle_war_insufficient_cards_p2():
    """Player 2 loses if they don't have enough cards for war"""
    p1_hand = deque([1, 2, 3, 4, 5])
    p2_hand = deque([6, 7])  # Only 2 cards, needs 4
    cards_in_play = [8, 8]
    stats = {'wars': 0, 'double_wars': 0, 'winner': None}
    
    result = handle_war(p1_hand, p2_hand, cards_in_play, stats)
    
    assert result is False
    assert stats['winner'] == 1


def test_handle_war_double_war():
    """Should handle war within a war (double war)"""
    p1_hand = deque([1, 2, 3, 5, 6, 7, 8, 14])  # 5 then 14
    p2_hand = deque([9, 10, 11, 5, 12, 13, 14, 7])  # 5 then 7
    cards_in_play = [4, 4]
    stats = {'wars': 0, 'double_wars': 0, 'winner': None}
    
    result = handle_war(p1_hand, p2_hand, cards_in_play, stats)
    
    assert result is True
    assert stats['double_wars'] == 1
    assert stats['wars'] == 1  # The recursive war increments this


def test_play_game_completes():
    """A full game should complete and return valid statistics"""
    stats = play_game()
    
    assert 'rounds' in stats
    assert 'wars' in stats
    assert 'double_wars' in stats
    assert 'winner' in stats
    assert 'hit_max_rounds' in stats
    assert stats['winner'] in [1, 2, None]
    assert stats['rounds'] > 0
    assert len(stats['p1_stack_sizes']) == stats['rounds'] + 1  # +1 for initial
    assert len(stats['p2_stack_sizes']) == stats['rounds'] + 1


def test_play_game_statistics_validity():
    """Game statistics should be internally consistent"""
    stats = play_game()
    
    # If game didn't hit max rounds, there should be a winner
    if not stats['hit_max_rounds']:
        assert stats['winner'] in [1, 2]
    
    # Wars count should be non-negative
    assert stats['wars'] >= 0
    assert stats['double_wars'] >= 0
    
    # Double wars can't exceed wars
    assert stats['double_wars'] <= stats['wars']
    
    # Max stack sizes should be reasonable
    assert stats['max_stack_p1'] <= 52
    assert stats['max_stack_p2'] <= 52