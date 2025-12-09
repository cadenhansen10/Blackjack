#!/usr/bin/env python3

from dataclasses import dataclass
import random

@dataclass
class Player:
    id: int
    name: str
    balance: float
    wins: int = 0
    losses: int = 0

class Card:
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value
        self.hidden = False

    def __str__(self):
        if self.hidden:
            return "Unknown"
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.__cards = []
        self.build()

    def build(self):
        self.__cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "Jack": 10, "Queen": 10, "King": 10, "Ace": 11
        }
        for suit in suits:
            for rank, value in ranks.items():
                self.__cards.append(Card(rank, suit, value))
    
    def shuffle(self):
        random.shuffle(self.__cards)

    def deal(self):
        if len(self.__cards) > 0:
            return self.__cards.pop()
        else:
            return None
            
    @property
    def count(self):
        return len(self.__cards)

class Hand:
    def __init__(self):
        self.__cards = []

    def add_card(self, card):
        self.__cards.append(card)

    @property
    def cards(self):
        return self.__cards

    @property
    def points(self):
        points = 0
        ace_count = 0
        
        for card in self.__cards:
            if not card.hidden:
                points += card.value
                if card.rank == "Ace":
                    ace_count += 1
        
        # Adjust for Aces if over 21
        while points > 21 and ace_count > 0:
            points -= 10
            ace_count -= 1
            
        return points

    def clear(self):
        self.__cards = []

    def __iter__(self):
        for card in self.__cards:
            yield card
