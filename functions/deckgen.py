import random
from count import calculate_hand_value

#Create a dictionary which relates the value of the playing card with the corresponding blackjack value
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

#Create a dictionary associating the value of playing card with how much the card adds to the count
counting_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1,
    'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

def create_deck():
    """
    Creates a deck consisting of 6 standard 52-card decks as is standard in a casino
    :return:
    """
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [f"{rank} of {suit}" for suit in suits for rank in card_values.keys()] * 6 #This creates 6 decks of 52 cards
    random.shuffle(deck) #This shuffles the deck we created before to randomise for the game start
    return deck

def deal_initial_cards(deck):
    """
    Deals two cards to both the player and dealer
    :param deck: the deck which was created in the above function
    :return:
    """
    return [deck.pop(), deck.pop()], [deck.pop(), deck.pop()] #Represents the two cards the player and dealer is dealt, then deleted from the deck so as to not be repeated

def display_hand(player, hand, hide_first_card=False):
    """
    Displays the hand which is dealt to the player and for the dealer
    :param player:
    :param hand:
    :param hide_first_card:
    :return:
    """
    if hide_first_card:
        print(f"{player}'s hand: [Hidden], {hand[1]}")
    else:
        print(f"{player}'s hand: {', '.join(hand)} (Value: {calculate_hand_value(hand)})")

def format_card(card):
    """Formats card string with suit emojis.

    Args:
        card (str): The card string (e.g., '10 of Hearts').

    Returns:
        str: The formatted card string with an emoji (e.g., '10♥️').
    """
    # Define card suit emojis for display
    suit_emojis = {
        "Hearts": "♥️",
        "Diamonds": "♦️",
        "Clubs": "♣️",
        "Spades": "♠️"
    }
    rank, suit = card.split(" of ")
    return f"{rank}{suit_emojis[suit]}"