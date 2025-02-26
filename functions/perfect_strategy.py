from count import calculate_hand_value

def check_perfect_strategy(player_hand, dealer_hand, split=False):
    """Checks if the player's move aligns with perfect Blackjack strategy.

    Args:
        player_hand (list): List of player's card values.
        dealer_hand (list): List of dealer's card values.
        split (bool, optional): Whether the player has chosen to split. Defaults to False.

    Returns:
        bool: True if the move follows the perfect strategy, False otherwise.
    """
    player_value = calculate_hand_value(player_hand)
    dealer_upcard = dealer_hand[0].split()[0]  # Dealer's first card

    # Convert face cards to numerical values for easier strategy checking
    if dealer_upcard in ["J", "Q", "K"]:
        dealer_upcard = 10
    elif dealer_upcard == "A":
        dealer_upcard = 11
    else:
        # Ensure dealer's upcard is extracted properly without the suit emoji
        dealer_upcard = dealer_hand[0][:-1]  # Removes the last character (suit emoji)

        # Convert face cards to numerical values
        if dealer_upcard in ["J", "Q", "K"]:
            dealer_upcard = 10
        elif dealer_upcard == "A":
            dealer_upcard = 11
        else:
            dealer_upcard = int(dealer_upcard)  # Convert number cards normally

    # Define basic strategy rules (simplified, can be expanded)
    strategy = {
        (8, 9, 10, 11): "H",  # Always hit low hands
        (12,): "H" if dealer_upcard in (2, 3, 7, 8, 9, 10, 11) else "S",
        (13, 14, 15, 16): "H" if dealer_upcard in (7, 8, 9, 10, 11) else "S",
        (17, 18, 19, 20, 21): "S",  # Always stand on high hands
    }

    # Determine the correct move
    correct_move = "H" if player_value in strategy and strategy[player_value] == "H" else "S"

    # Special rule for splitting
    if split:
        return True  # Assume splitting is always correct when allowed

    return correct_move == ("H" if player_hand[-1] else "S")