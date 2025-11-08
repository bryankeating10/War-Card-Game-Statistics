import pytest
from analysis import analyze_results, print_summary
from io import StringIO
import sys


def test_analyze_results_empty():
    """Should handle empty list gracefully"""
    results = analyze_results([])
    assert results == {}


def test_analyze_results_single_game():
    """Should analyze a single game correctly"""
    game_stats = [{
        'rounds': 100,
        'wars': 5,
        'double_wars': 1,
        'winner': 1,
        'hit_max_rounds': False,
    }]
    
    results = analyze_results(game_stats)
    
    assert results['total_games'] == 1
    assert results['rounds']['mean'] == 100
    assert results['rounds']['median'] == 100
    assert results['wars']['mean'] == 5
    assert results['winners']['player_1_wins'] == 1
    assert results['winners']['player_2_wins'] == 0


def test_analyze_results_multiple_games():
    """Should correctly aggregate statistics from multiple games"""
    game_stats = [
        {
            'rounds': 100,
            'wars': 5,
            'double_wars': 0,
            'winner': 1,
            'hit_max_rounds': False,
        },
        {
            'rounds': 200,
            'wars': 10,
            'double_wars': 2,
            'winner': 2,
            'hit_max_rounds': False,
        },
        {
            'rounds': 150,
            'wars': 7,
            'double_wars': 1,
            'winner': 1,
            'hit_max_rounds': False,
        },
    ]
    
    results = analyze_results(game_stats)
    
    assert results['total_games'] == 3
    assert results['rounds']['mean'] == 150  # (100 + 200 + 150) / 3
    assert results['rounds']['median'] == 150
    assert results['rounds']['min'] == 100
    assert results['rounds']['max'] == 200
    assert results['wars']['mean'] == pytest.approx(7.333, rel=0.01)
    assert results['winners']['player_1_wins'] == 2
    assert results['winners']['player_2_wins'] == 1


def test_analyze_results_win_percentages():
    """Should calculate win percentages correctly"""
    game_stats = [
        {'rounds': 100, 'wars': 5, 'double_wars': 0, 'winner': 1, 
         'hit_max_rounds': False},
        {'rounds': 200, 'wars': 10, 'double_wars': 2, 'winner': 1, 
         'hit_max_rounds': False},
        {'rounds': 150, 'wars': 7, 'double_wars': 1, 'winner': 2, 
         'hit_max_rounds': False},
        {'rounds': 175, 'wars': 8, 'double_wars': 1, 'winner': 2, 
         'hit_max_rounds': False}
    ]
    
    results = analyze_results(game_stats)
    
    assert results['winners']['player_1_wins'] == 2
    assert results['winners']['player_2_wins'] == 2
    assert results['winners']['player_1_win_percentage'] == 50.0
    assert results['winners']['player_2_win_percentage'] == 50.0


def test_analyze_results_games_with_wars():
    """Should track games with wars correctly"""
    game_stats = [
        {'rounds': 100, 'wars': 5, 'double_wars': 0, 'winner': 1,
         'hit_max_rounds': False},
        {'rounds': 200, 'wars': 0, 'double_wars': 0, 'winner': 2,
         'hit_max_rounds': False},
        {'rounds': 150, 'wars': 3, 'double_wars': 1, 'winner': 1,
         'hit_max_rounds': False}
    ]
    
    results = analyze_results(game_stats)
    
    assert results['wars']['games_with_wars'] == 2
    assert results['wars']['percentage_with_wars'] == pytest.approx(66.67, rel=0.01)
    assert results['double_wars']['games_with_double_wars'] == 1
    assert results['double_wars']['percentage_with_double_wars'] == pytest.approx(33.33, rel=0.01)


def test_analyze_results_infinite_games():
    """Should track games that hit max rounds"""
    game_stats = [
        {'rounds': 100, 'wars': 5, 'double_wars': 0, 'winner': 1,
         'hit_max_rounds': False},
        {'rounds': 100000, 'wars': 0, 'double_wars': 0, 'winner': None,
         'hit_max_rounds': True},
        {'rounds': 150, 'wars': 3, 'double_wars': 1, 'winner': 2,
         'hit_max_rounds': False}
    ]
    
    results = analyze_results(game_stats)
    
    assert results['infinite_games']['count'] == 1
    assert results['infinite_games']['percentage'] == pytest.approx(33.33, rel=0.01)

def test_print_summary_empty():
    """Should handle empty results gracefully"""
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    print_summary({})
    
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    
    assert "No results to display" in output


def test_print_summary_with_results():
    """Should print formatted summary without errors"""
    results = {
        'total_games': 100,
        'rounds': {'mean': 150.5, 'median': 145.0, 'stdev': 25.3, 'min': 50, 'max': 300},
        'wars': {'mean': 7.2, 'median': 7.0, 'stdev': 3.1, 'min': 0, 'max': 20,
                'games_with_wars': 95, 'percentage_with_wars': 95.0},
        'double_wars': {'mean': 1.5, 'median': 1.0, 'stdev': 1.2, 'min': 0, 'max': 5,
                       'games_with_double_wars': 60, 'percentage_with_double_wars': 60.0},
        'winners': {'player_1_wins': 52, 'player_2_wins': 48,
                   'player_1_win_percentage': 52.0, 'player_2_win_percentage': 48.0},
        'infinite_games': {'count': 0, 'percentage': 0.0},
        'correlation_wars_rounds': 0.65,
    }
    
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    print_summary(results)
    
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    
    # Check that key sections are present
    assert "WAR CARD GAME SIMULATION RESULTS" in output
    assert "Total Games Simulated: 100" in output
    assert "GAME LENGTH" in output
    assert "WARS" in output
    assert "WINNERS" in output