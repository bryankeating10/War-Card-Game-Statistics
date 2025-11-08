from typing import Dict, Any
import pandas as pd
from game import play_game
from analysis import analyze_results


def run_simulation(num_games: int = 10000, verbose: bool = True) -> Dict[str, Any]:
    """
    Run multiple War game simulations and return aggregate statistics.
    
    Args:
        num_games: Number of games to simulate
        verbose: Whether to print progress updates
    
    Returns:
        Dictionary containing:
            - 'game_data': DataFrame with individual game statistics (indexed by game_num)
            - 'summary': Dictionary of aggregate statistics from analyze_results()
    """
    if verbose:
        print(f"\nRunning {num_games:,} War game simulations...")
        print("This may take a moment...\n")
    
    all_game_stats = []
    
    # Progress reporting intervals
    report_interval = max(1, num_games // 10)  # Report every 10%
    
    for i in range(num_games):
        # Run a single game
        game_stats = play_game()
        game_stats['game_num'] = i + 1  # Add game number starting from 1
        all_game_stats.append(game_stats)
        
        # Progress update
        if verbose and (i + 1) % report_interval == 0:
            progress = ((i + 1) / num_games) * 100
            print(f"Progress: {progress:.0f}% ({i + 1:,} / {num_games:,} games)")
    
    if verbose:
        print(f"\nCompleted {num_games:,} simulations!")
        print("Analyzing results...\n")
    
    # Convert to DataFrame
    # Extract only the scalar values for the main DataFrame
    df_data = []
    for game in all_game_stats:
        row = {
            'game_num': game['game_num'],
            'rounds': game['rounds'],
            'wars': game['wars'],
            'double_wars': game['double_wars'],
            'winner': game['winner'],
            'hit_max_rounds': game['hit_max_rounds'],
            'max_stack_p1': game['max_stack_p1'],
            'max_stack_p2': game['max_stack_p2'],
        }
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    df.set_index('game_num', inplace=True)
    
    # Analyze and return results
    summary = analyze_results(all_game_stats)
    
    return {
        'game_data': df,
        'summary': summary
    }