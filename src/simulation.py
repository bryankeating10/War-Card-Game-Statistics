from typing import List, Dict, Any
from src.game import play_game
from src.analysis import analyze_results


def run_simulation(num_games: int = 10000, verbose: bool = True) -> Dict[str, Any]:
    """
    Run multiple War game simulations and return aggregate statistics.
    
    Args:
        num_games: Number of games to simulate
        verbose: Whether to print progress updates
    
    Returns:
        Dictionary containing aggregate statistics across all games
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
        all_game_stats.append(game_stats)
        
        # Progress update
        if verbose and (i + 1) % report_interval == 0:
            progress = ((i + 1) / num_games) * 100
            print(f"Progress: {progress:.0f}% ({i + 1:,} / {num_games:,} games)")
    
    if verbose:
        print(f"\nCompleted {num_games:,} simulations!")
        print("Analyzing results...\n")
    
    # Analyze and return results
    results = analyze_results(all_game_stats)
    
    return results