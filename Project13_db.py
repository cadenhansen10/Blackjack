#!/usr/bin/env python3

import sqlite3
from contextlib import closing
from Project13_business import Player

# Database connection global
conn = None
DB_FILE = "blackjack.sqlite"

def connect():
    """Connect to the SQLite database and create tables if they don't exist."""
    global conn
    if not conn:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        create_tables()

def close():
    """Close the database connection."""
    if conn:
        conn.close()

def create_tables():
    """Create necessary tables for the game."""
    query = '''CREATE TABLE IF NOT EXISTS Player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                balance REAL DEFAULT 1000.0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
               )'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        conn.commit()

def get_player(name):
    """Retrieve a player by name, or create if not exists."""
    query = '''SELECT id, name, balance, wins, losses 
               FROM Player WHERE name = ?'''
    
    with closing(conn.cursor()) as c:
        c.execute(query, (name,))
        row = c.fetchone()
        
        if row:
            return Player(row["id"], row["name"], row["balance"], row["wins"], row["losses"])
        else:
            # Create new player
            insert_sql = '''INSERT INTO Player (name, balance) VALUES (?, ?)'''
            c.execute(insert_sql, (name, 1000.0)) # Default 1000 starting balance
            conn.commit()
            return get_player(name)

def update_player_balance(player, amount, win=False, loss=False):
    """Update player balance and stats."""
    # amount is the change (positive or negative)
    new_balance = player.balance + amount
    
    wins_inc = 1 if win else 0
    losses_inc = 1 if loss else 0
    
    sql = '''UPDATE Player 
             SET balance = ?, wins = wins + ?, losses = losses + ?
             WHERE id = ?'''
             
    with closing(conn.cursor()) as c:
        c.execute(sql, (new_balance, wins_inc, losses_inc, player.id))
        conn.commit()
    
    # Update the local object as well
    player.balance = new_balance
    player.wins += wins_inc
    player.losses += losses_inc

def main():
    connect()
    print("Database setup complete.")
    close()

if __name__ == "__main__":
    main()
