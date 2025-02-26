# Create a dictionary which relates the value of the playing card with the corresponding blackjack value
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

#Create a dictionary associating the value of playing card with how much the card adds to the count
counting_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1,
    'J': -1, 'Q': -1, 'K': -1, 'A': -1
}


def calculate_hand_value(hand):
    """
    Calculates the value of a blackjack hand, correctly handling Aces.

    :parameters:
        hand (list): List of card strings formatted with emojis (10♥️', 'A♠️').

    Returns:
        int: The total value of the hand.
    """
    value = 0
    ace_count = 0

    # Dictionary to extract numeric rank (removing emoji)
    emoji_card_map = {f"{rank}{suit}": rank for suit in ["♥️", "♦️", "♣️", "♠️"] for rank in
                      ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']}

    for card in hand:
        rank = emoji_card_map.get(card, card[:-1])  # Use dictionary or fallback to slicing

        if rank in ["J", "Q", "K"]:
            value += 10
        elif rank == "A":
            value += 11
            ace_count += 1
        else:
            value += int(rank)

    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1

    return value

def update_count(hand, count):
    """
    Updates the card count based on the dealt hand
    :param hand:
    :param count:
    :return:
    """
    for card in hand:
        rank = card.split()[0]
        count += counting_values[rank]
    return count

