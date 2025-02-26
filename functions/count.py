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
    value = 0 #Initialise the value of the hand
    ace_count = 0 #Initialise the counting of aces for the hand, will be explained later

    # Dictionary to extract numeric rank (removing emoji)
    emoji_card_map = {f"{rank}{suit}": rank for suit in ["♥️", "♦️", "♣️", "♠️"] for rank in
                      ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']}

    for card in hand: #iterating for every card in the hand list
        rank = emoji_card_map.get(card, card[:-1])  # Use dictionary or fallback to slicing

        if rank in ["J", "Q", "K"]: #If the rank of the card is a Jack Queen or King respectiverly
            value += 10 #The value we add will be 10 to the hand
        elif rank == "A": #If the card is an ace
            value += 11 #We add an 11 to the value of the hand
            ace_count += 1 #Important to track aces in the scenario you draw aces and bust immediately
        else:
            value += int(rank)#Otherwise, we just add the value of the card (i.e. 2 = int(2), 3 = int(3) etc.)

    while value > 21 and ace_count: #while the value of your hand is greater than 21 (so you bust) and you have aces
        value -= 10 #We switch the value of the ace to instead be 1 instead of 11, thus why we subtract 10
        ace_count -= 1 #We redo the ace_count

    return value

def update_count(hand, count):
    """
    A function which will be used to continuously update the card count based on the dealt hand
    :param hand: the hand list parameter which is generated for the player and the dealer
    :param count: integer parameter which will hold the running count of the game
    :return:
    """
    for card in hand: #We first loop through every card which is present in the active hands of the player and the dealer
        rank = card.split()[0]#We split it and find the first element of the card, which will be the value
        count += counting_values[rank] #According to that, we then add what the corresponding count is from the counting_values dictionary crerated before
    return count #This thus returns the current running count of the game, and will be added upon with each hand dealt.

