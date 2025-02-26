def check_basic_strategy(player_hand, dealer_hand):
    """
    Checks if the player's move aligns with basic blackjack strategy.
    Covers hard hands and soft hands based on the provided strategy chart.

    :Parameters:
        player_hand (list of str): List of player's card strings with emoji suits.
        dealer_hand (list of str): List of dealer's card strings with emoji suits.

    Returns:
        str: "hit" or "stand" based on the correct basic strategy.
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

    # **Soft Hands (Contains an Ace as 11)**
    if "A" in player_ranks and sum(player_values) <= 21:  # Ensure soft hand check
        if player_total <= 17:
            return "hit"
        elif player_total == 18:
            return "stand" if dealer_upcard in [2, 7, 8] else "hit"
        else:
            return "stand"

    # **Hard Hands (No Ace or Ace counts as 1)**
    if player_total >= 17:
        return "stand"  # Always stand on 17+
    elif player_total == 16:
        return "stand" if dealer_upcard in [2, 3, 4, 5, 6] else "hit"
    elif player_total == 15:
        return "stand" if dealer_upcard in [2, 3, 4, 5, 6] else "hit"
    elif player_total == 14:
        return "stand" if dealer_upcard in [2, 3, 4, 5, 6] else "hit"
    elif player_total == 13:
        return "stand" if dealer_upcard in [2, 3, 4, 5, 6] else "hit"
    elif player_total == 12:
        return "stand" if dealer_upcard in [4, 5, 6] else "hit"
    else:
        return "hit"  # Always hit on 11 or lower