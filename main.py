#!/usr/bin/env python3
"""
War Card Game Simulation

This program simulates thousands of games of War (the card game) 
and provides statistical analysis of emergent behaviors including:
- Average game length
- Number of wars and double wars
- Player stack size distributions
- Correlation between wars and game length
"""

import argparse
from src.simulation import run_simulation
from src.analysis import print_summary


def main():
    """Main entry point for the War game simulation."""
    parser = argparse.ArgumentParser(
        description='Simulate War card games and analyze statistics'
    )
    parser.add_argument(
        '-n', '--num-games',
        type=int,
        default=10000,
        help='Number of games to simulate (default: 10000)'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress progress messages'
    )
    
    args = parser.parse_args()
    
    # Run simulation
    results = run_simulation(
        num_games=args.num_games,
        verbose=not args.quiet
    )
    
    # Print results
    print_summary(results)


if __name__ == "__main__":
    main()