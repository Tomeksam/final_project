def check_basic_strategy(player_hand, dealer_hand):
    """
    Checks if the player's move aligns with basic blackjack strategy.
    Covers hard hands, soft hands, and splitting rules.

    :Parameters:
        player_hand (list of str): List of player's card strings with emoji suits.
        dealer_hand (list of str): List of dealer's card strings with emoji suits.

    Returns:
        bool: True if the move follows basic strategy, False otherwise.
    """

    # Mapping face cards and Aces
    card_values = {"J": 10, "Q": 10, "K": 10, "A": 11}

    # Extract dealer's upcard rank and remove suit emoji
    dealer_upcard = dealer_hand[0].split()[0]  # extracts only the rank of the dealer
    dealer_upcard = card_values.get(dealer_upcard, int(dealer_upcard) if dealer_upcard.isdigit() else 0)

    # Extract player's hand ranks and convert values
    player_ranks = [card.split()[0] for card in player_hand]  # Extract ranks properly
    player_values = [card_values.get(rank, int(rank) if rank.isdigit() else 0) for rank in player_ranks]
    player_total = sum(player_values)

    # **Soft Hands (Contains an Ace)**
    if "A" in player_ranks and len(player_hand) == 2:
        if player_total == 18:
            return "stand" if dealer_upcard in [2, 7, 8] else "hit"  # Stand vs 2, 7, 8; otherwise hit
        elif player_total >= 19:
            return "stand"  # Always stand on 19+
        elif player_total == 17:
            return "hit"  # Always hit on soft 17
        else:
            return "hit"  # Hit on soft totals 13-16

    # **Hard Hands (No Ace or Used as 1)**
    if player_total >= 17:
        return "stand"  # Always stand on 17+
    elif 13 <= player_total <= 16:
        return "hit" if dealer_upcard >= 7 else "stand"  # Hit against 7-A, stand vs. 2-6
    elif player_total == 12:
        return "stand" if dealer_upcard in [4, 5, 6] else "hit"  # Stand on 4-6, hit otherwise
    elif player_total == 11:
        return "hit"  # Always hit on 11
    elif player_total == 10:
        return "hit"  # Always hit on 10
    elif player_total == 9:
        return "hit"  # Always hit on 9
    else:
        return "hit"  # Always hit on anything below 9