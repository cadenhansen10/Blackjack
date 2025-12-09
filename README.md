# Project 13: Blackjack Pro - User Guide

## Introduction
Welcome to **Blackjack Pro**! This is a modern, graphical simulation of the classic casino card game using Python. It features a rich interface and long-term stat tracking.

## Getting Started

### 1. Launching the Game
Open your terminal and run:
```bash
python3 Project13_gui.py
```

### 2. Login
*   **Enter Name**: Type your name in the flashing box.
*   **Rules**: Only letters, numbers, and spaces are allowed.
    *   *Good*: "John Doe", "Player1"
    *   *Bad*: "Winner!", "User#1"

### 3. Project Logic
*   **Project13_business.py**: Defines the core data models: 
    - `Player`: Stores your persistent stats (ID, Name, Balance, Wins, Losses).
    - `Card`, `Deck`, `Hand`: Logic for card management.
*   **Project13_db.py**: Handles saving your progress to the database (`blackjack.sqlite`), ensuring your wins, losses, and balance are safe.
*   **Project13_game.py**: The brain of the operation. It enforces the rules of Blackjack (e.g., dealer hits on 16).
*   **Project13_gui.py**: The visual interface. It uses the data from the business layer to calculate and display:
    - **Win Rate**: Calculated from your total wins vs. total games.
    - **Net Earnings**: Shows how much you've won or lost relative to the starting $1000.

## How to Play

1.  **Place Your Bet**: 
    *   Enter an amount (e.g., `20`) in the white box.
    *   Click the purple **DEAL** button.
    *   *Tip*: Your bet is locked in once the hand starts.



3.  **Your Turn**:
    *   **HIT (Blue Button)**: Draw another card to get closer to 21. Watch out—if you go over 21, you **BUST** and lose immediately.
    *   **STAND (Yellow Button)**: Keep your current hand and let the Dealer play to try and beat you.

4.  **Dealer's Turn**:
    *   The dealer reveals their hidden card.
    *   They MUST **draw** until they reach at least **16**.
    *   They MUST **stop** (stand) on **17** or higher.


5.  **Winning**:
    *   **Win**: Beat the dealer's score without busting. (Pays 1:1)
    *   **Blackjack**: Get 21 on your first two cards. (Pays 3:2)
    *   **Dealer Busts**: If the dealer goes over 21, you win automatically!

## Features to Look For
*   **Visuals**: Gold-bordered face cards, suit symbols on the table, and a realistic "shoe" deck.
*   **Persistent Stats**: The database tracks your **Total Wins** and **Losses** forever.
    *   **Win Rate**: Calculated automatically from your history.
    *   **Net Earnings**: Shows your total lifetime profit/loss based on your balance.


## Requirements
*   Python 3
*   (Mac Users) `tkmacosx` recommended for best visuals, but valid without it.

**Good Luck at the Tables!**
