#!/usr/bin/env python3

from Project13_business import Deck, Hand

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.is_game_over = False

    def start_new_hand(self):
        """Resets hands and deals initial cards."""
        self.deck.build() # Rebuild deck each hand (standard for simple online blackjack)
        self.deck.shuffle()
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.is_game_over = False

        # Deal 2 cards each
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        
        self.dealer_hand.add_card(self.deck.deal())
        hidden_card = self.deck.deal()
        hidden_card.hidden = True
        self.dealer_hand.add_card(hidden_card)

    def player_hit(self):
        """Deals a card to the player. Returns True if player busts."""
        if self.is_game_over:
            return False
            
        self.player_hand.add_card(self.deck.deal())
        
        if self.player_hand.points > 21:
            self.is_game_over = True
            return True # Bust
        return False

    def dealer_turn(self):
        """Executes dealer's turn. Dealer hits until >= 17."""
        # Reveal hidden card
        for card in self.dealer_hand:
            card.hidden = False
            
        while self.dealer_hand.points < 17:
            self.dealer_hand.add_card(self.deck.deal())
            
        self.is_game_over = True

    def get_result(self):
        """Determines the result of the game. Returns (winner_string, payout_multiplier)."""
        player_points = self.player_hand.points
        dealer_points = self.dealer_hand.points

        if player_points > 21:
            return "Dealer Wins! (Player Bust)", 0
        
        if dealer_points > 21:
            return "Player Wins! (Dealer Bust)", 2.0
            
        if player_points > dealer_points:
            if player_points == 21 and len(self.player_hand.cards) == 2:
                return "Blackjack Wins 3:2!", 2.5
            return "Player Wins!", 2.0
            
        elif dealer_points > player_points:
            return "Dealer Wins!", 0
        else:
            return "Push (Tie)", 1.0

