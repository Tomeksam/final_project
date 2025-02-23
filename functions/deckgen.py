import random
from functions.count import *

# Define the deck with card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Card counting system values
counting_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1,
    'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

def create_deck():
    """Creates a deck consisting of 6 standard 52-card decks."""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [f"{rank} of {suit}" for suit in suits for rank in card_values.keys()] * 6
    random.shuffle(deck)
    return deck

def deal_initial_cards(deck):
    """Deals two cards to both the player and dealer."""
    return [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]

def display_hand(player, hand, hide_first_card=False):
    """Displays a player's hand."""
    if hide_first_card:
        print(f"{player}'s hand: [Hidden], {hand[1]}")
    else:
        print(f"{player}'s hand: {', '.join(hand)} (Value: {calculate_hand_value(hand)})")

