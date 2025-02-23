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

def calculate_hand_value(hand):
    """Calculates the value of a hand, handling Aces properly."""
    value = sum(card_values[card.split()[0]] for card in hand)
    ace_count = sum(1 for card in hand if card.startswith('A'))
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1
    return value

def update_count(hand, count):
    """Updates the card count based on the dealt hand."""
    for card in hand:
        rank = card.split()[0]
        count += counting_values[rank]
    return count

