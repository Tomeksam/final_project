import random # using random library for deck generation
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
    :return: deck (a list)
    """
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [f"{rank} of {suit}" for suit in suits for rank in card_values.keys()] * 6 #This creates 6 decks of 52 cards; iterates over suits and card values to pair them up
    random.shuffle(deck) #This shuffles the deck we created before to randomise for the game start; uses uniform probability distribution
    return deck

def deal_initial_cards(deck):
    """
    Deals two cards to both the player and dealer
    :param deck: the deck which was created in the above function
    :return: 2 lists with 2 cards each popped from the deck
    """
    return [deck.pop(), deck.pop()], [deck.pop(), deck.pop()] #Represents the two cards the player and dealer is dealt, then deleted from the deck so as to not be repeated
    # .pop() removes last item from deck; deck permanently altered with that card removed (lists are mutable)

def display_hand(player, hand, hide_first_card=False):
    """
    Displays the hand which is dealt to the player and for the dealer
    :param player: "Player" or "Dealer" (whose deck should be displayed)
    :param hand: either player_hand or dealer_hand; from which deck will formatted cards be displayed
    :param hide_first_card: Boolean parameter (True to hide dealer's first card & default False for player)
    :return:
    """
    if hide_first_card: # if hide_first_card is true
        print(f"{player}'s hand: [Hidden], {hand[1]}") # For dealer print [Hidden] for the first card and only display the 2nd card
    else: # case where hide_first_card is false
        print(f"{player}'s hand: {', '.join(hand)} (Value: {calculate_hand_value(hand)})") # For the "Player" (could be player/dealer) displays entire deck through .join(hand) and also the value of the hand


def format_card(card):
    """Ensures card is formatted correctly with suit emojis.

    :parameter
        card

    Returns:
        str: The formatted card string with an emoji
    """
    # Mapping of suits to emojis using a dictionary
    suit_emojis = {
        "Hearts": "♥️",
        "Diamonds": "♦️",
        "Clubs": "♣️",
        "Spades": "♠️"
    }

    # If the card is already formatted with an emoji, return it as is
    if any(suit in card for suit in suit_emojis.values()): # if card already contains emoji
        return card  # Prevents reformatting an already formatted card

    # Standard formatting for new cards
    if " of " in card:  # Ensures only standard cards are formatted
        rank, suit = card.split(" of ") # splits by "of" to assign values to variables rank & suit
        return f"{rank}{suit_emojis[suit]}" # uses name of suit to index dictionary and replace with the emoji (the dictionary value)
    else:
        return card  # If unexpected format, return as is
