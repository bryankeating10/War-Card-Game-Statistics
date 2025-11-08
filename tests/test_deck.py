import pytest
from src.deck import create_deck, deal_cards, CARD_RANKS

def test_create_deck_size():
    """Deck should have exactly 52 cards"""
    deck = create_deck()
    assert len(deck) == 52

def test_create_deck_composition():
    """Deck should have 4 of each rank"""
    deck = create_deck()
    for rank in CARD_RANKS:
        assert deck.count(rank) == 4

def test_deal_cards_equal_split():
    """Each player should get 26 cards"""
    deck = create_deck()
    p1, p2 = deal_cards(deck)
    assert len(p1) == 26
    assert len(p2) == 26

def test_deal_cards_no_duplicates():
    """All 52 cards should be dealt (no loss/duplication)"""
    deck = create_deck()
    p1, p2 = deal_cards(deck)
    combined = list(p1) + list(p2)
    assert sorted(combined) == sorted(deck)

def test_deal_cards_randomness():
    """Multiple deals should produce different results"""
    deck = create_deck()
    p1_first, _ = deal_cards(deck)
    p1_second, _ = deal_cards(deck)
    # Very unlikely to be identical if properly shuffled
    assert list(p1_first) != list(p1_second)

def test_deal_cards_returns_deques():
    """Should return deque objects for efficient operations"""
    from collections import deque
    deck = create_deck()
    p1, p2 = deal_cards(deck)
    assert isinstance(p1, deque)
    assert isinstance(p2, deque)