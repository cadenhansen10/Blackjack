#!/usr/bin/env python3

import os
import Project13_db as db
from Project13_game import BlackjackGame
from Project13_business import Player

def test_db():
    print("Testing Database...")
    db.connect()
    
    # Test Player Creation
    name = "TestPlayer_" + str(os.getpid())
    player = db.get_player(name)
    assert player.name == name
    assert player.balance == 1000.0 # Default
    print(f"  [PASS] Player creation (Balance: {player.balance})")

    # Test Balance Update
    db.update_player_balance(player, -50.0)
    # Re-fetch to verify persistence
    player = db.get_player(name)
    assert player.balance == 950.0
    print(f"  [PASS] Balance deduction (New Balance: {player.balance})")
    
    db.update_player_balance(player, 100.0, win=True)
    player = db.get_player(name)
    assert player.balance == 1050.0
    assert player.wins == 1
    print(f"  [PASS] Win update (New Balance: {player.balance}, Wins: {player.wins})")
    
    db.close()

def test_game_logic():
    print("\nTesting Game Logic...")
    game = BlackjackGame()
    
    # Test Start Hand
    game.start_new_hand()
    assert len(game.player_hand.cards) == 2
    assert len(game.dealer_hand.cards) == 2
    print(f"  [PASS] Initial Deal (Player: {game.player_hand.points}, Dealer: ?)")

    # Test Hit
    points_before = game.player_hand.points
    game.player_hit()
    assert len(game.player_hand.cards) == 3
    print(f"  [PASS] Player Hit (New points: {game.player_hand.points})")

    # Test Deck Shuffle/Rebuild
    game.start_new_hand()
    assert game.deck.count < 52 # Should be 52 minus dealt cards
    print(f"  [PASS] Deck usage (Cards remaining: {game.deck.count})")

def main():
    try:
        test_db()
        test_game_logic()
        print("\nAll automated verification tests PASSED.")
    except AssertionError as e:
        print(f"\n[FAIL] Verification failed: {e}")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
