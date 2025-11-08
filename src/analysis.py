import statistics
from typing import List, Dict, Any


def analyze_results(all_game_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze statistics from multiple game simulations, excluding infinite games
    from all metrics except their own count.
    """
    if not all_game_stats:
        return {}

    # Separate finite and infinite games
    finite_games = [g for g in all_game_stats if not g['hit_max_rounds']]
    infinite_games = [g for g in all_game_stats if g['hit_max_rounds']]

    # Edge case: if all games are infinite
    if not finite_games:
        return {
            'total_games': len(all_game_stats),
            'rounds': {},
            'wars': {},
            'double_wars': {},
            'winners': {},
            'max_stacks': {},
            'correlation_wars_rounds': None,
            'infinite_games': {
                'count': len(infinite_games),
                'percentage': 100.0,
            },
        }

    # Extract finite game data
    rounds = [g['rounds'] for g in finite_games]
    wars = [g['wars'] for g in finite_games]
    double_wars = [g['double_wars'] for g in finite_games]
    max_stack_p1 = [g['max_stack_p1'] for g in finite_games]
    max_stack_p2 = [g['max_stack_p2'] for g in finite_games]

    # Winner analysis (finite games only)
    p1_wins = sum(1 for g in finite_games if g['winner'] == 1)
    p2_wins = sum(1 for g in finite_games if g['winner'] == 2)

    # Games with wars (finite only)
    games_with_wars = sum(1 for g in finite_games if g['wars'] > 0)
    games_with_double_wars = sum(1 for g in finite_games if g['double_wars'] > 0)

    total_games = len(all_game_stats)
    total_finite = len(finite_games)
    total_infinite = len(infinite_games)

    # Compile results
    results = {
        'total_games': total_games,
        'rounds': {
            'mean': statistics.mean(rounds),
            'median': statistics.median(rounds),
            'stdev': statistics.stdev(rounds) if len(rounds) > 1 else 0,
            'min': min(rounds),
            'max': max(rounds),
        },
        'wars': {
            'mean': statistics.mean(wars),
            'median': statistics.median(wars),
            'stdev': statistics.stdev(wars) if len(wars) > 1 else 0,
            'min': min(wars),
            'max': max(wars),
            'games_with_wars': games_with_wars,
            'percentage_with_wars': (games_with_wars / total_finite) * 100,
        },
        'double_wars': {
            'mean': statistics.mean(double_wars),
            'median': statistics.median(double_wars),
            'stdev': statistics.stdev(double_wars) if len(double_wars) > 1 else 0,
            'min': min(double_wars),
            'max': max(double_wars),
            'games_with_double_wars': games_with_double_wars,
            'percentage_with_double_wars': (games_with_double_wars / total_finite) * 100,
        },
        'winners': {
            'player_1_wins': p1_wins,
            'player_2_wins': p2_wins,
            'player_1_win_percentage': (p1_wins / total_finite) * 100,
            'player_2_win_percentage': (p2_wins / total_finite) * 100,
        },
        'max_stacks': {
            'p1_mean': statistics.mean(max_stack_p1),
            'p1_median': statistics.median(max_stack_p1),
            'p1_max': max(max_stack_p1),
            'p2_mean': statistics.mean(max_stack_p2),
            'p2_median': statistics.median(max_stack_p2),
            'p2_max': max(max_stack_p2),
        },
        'infinite_games': {
            'count': total_infinite,
            'percentage': (total_infinite / total_games) * 100,
        },
    }

    # Correlation (finite games only)
    if len(rounds) > 1 and len(wars) > 1:
        try:
            mean_rounds = statistics.mean(rounds)
            mean_wars = statistics.mean(wars)
            numerator = sum((r - mean_rounds) * (w - mean_wars) for r, w in zip(rounds, wars))
            denominator = (
                sum((r - mean_rounds) ** 2 for r in rounds) ** 0.5 *
                sum((w - mean_wars) ** 2 for w in wars) ** 0.5
            )
            results['correlation_wars_rounds'] = numerator / denominator if denominator != 0 else 0
        except Exception:
            results['correlation_wars_rounds'] = None
    else:
        results['correlation_wars_rounds'] = None

    return results

def print_summary(results: Dict[str, Any]) -> None:
    """Print a formatted summary of simulation results."""
    if not results:
        print("No results to display.")
        return

    print("\n" + "=" * 70)
    print("WAR CARD GAME SIMULATION RESULTS")
    print("=" * 70)
    print(f"\nTotal Games Simulated: {results['total_games']:,}")

    print("\n(Note: Statistics below exclude infinite games.)")

    # Game length stats
    r = results.get('rounds', {})
    if r:
        print("\n" + "-" * 70)
        print("GAME LENGTH (rounds)")
        print("-" * 70)
        print(f"  Mean:     {r['mean']:>10.2f}")
        print(f"  Median:   {r['median']:>10.2f}")
        print(f"  Std Dev:  {r['stdev']:>10.2f}")
        print(f"  Min:      {r['min']:>10,}")
        print(f"  Max:      {r['max']:>10,}")

    # Wars stats
    w = results.get('wars', {})
    if w:
        print("\n" + "-" * 70)
        print("WARS")
        print("-" * 70)
        print(f"  Mean:     {w['mean']:>10.2f}")
        print(f"  Median:   {w['median']:>10.2f}")
        print(f"  Std Dev:  {w['stdev']:>10.2f}")
        print(f"  Min:      {w['min']:>10,}")
        print(f"  Max:      {w['max']:>10,}")
        print(f"  Games w/ Wars:      {w['games_with_wars']:>10,}")
        print(f"  % Games w/ Wars:    {w['percentage_with_wars']:>10.2f}%")

    # Double wars stats
    dw = results.get('double_wars', {})
    if dw:
        print("\n" + "-" * 70)
        print("DOUBLE WARS")
        print("-" * 70)
        print(f"  Mean:     {dw['mean']:>10.2f}")
        print(f"  Median:   {dw['median']:>10.2f}")
        print(f"  Std Dev:  {dw['stdev']:>10.2f}")
        print(f"  Min:      {dw['min']:>10,}")
        print(f"  Max:      {dw['max']:>10,}")
        print(f"  Games w/ Double Wars:   {dw['games_with_double_wars']:>10,}")
        print(f"  % Games w/ Double Wars: {dw['percentage_with_double_wars']:>10.2f}%")

    # Winners stats
    win = results.get('winners', {})
    if win:
        print("\n" + "-" * 70)
        print("WINNERS")
        print("-" * 70)
        print(f"  Player 1 Wins:  {win['player_1_wins']:>10,} ({win['player_1_win_percentage']:>5.2f}%)")
        print(f"  Player 2 Wins:  {win['player_2_wins']:>10,} ({win['player_2_win_percentage']:>5.2f}%)")

    # Stack stats
    stacks = results.get('max_stacks', {})
    if stacks:
        print("\n" + "-" * 70)
        print("MAX STACK SIZES")
        print("-" * 70)
        print(f"  P1 Mean:   {stacks['p1_mean']:>10.2f}   Median: {stacks['p1_median']:>10.2f}   Max: {stacks['p1_max']:>10,}")
        print(f"  P2 Mean:   {stacks['p2_mean']:>10.2f}   Median: {stacks['p2_median']:>10.2f}   Max: {stacks['p2_max']:>10,}")

    # Correlation
    if 'correlation_wars_rounds' in results:
        print("\n" + "-" * 70)
        print("CORRELATION")
        print("-" * 70)
        print(f"  Wars vs. Game Length: {results['correlation_wars_rounds']:>10.2f}")

    # Infinite games
    inf = results.get('infinite_games', {})
    if inf and inf.get('count', 0) > 0:
        print("\n" + "-" * 70)
        print("INFINITE GAMES (hit max rounds limit)")
        print("-" * 70)
        print(f"  Count:      {inf['count']:>10,}")
        print(f"  Percentage: {inf['percentage']:>10.2f}%")

    print("\n" + "=" * 70 + "\n")