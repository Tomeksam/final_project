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
    dealer_upcard = dealer_hand[0] if isinstance(dealer_hand, list) else dealer_hand #remove suits
    dealer_upcard = card_values.get(dealer_upcard, int(dealer_upcard) if dealer_upcard.isdigit() else 0)

    # Extract player's hand ranks and convert values
    player_ranks = [card.split()[0] for card in player_hand]  # Extract ranks properly
    player_values = [card_values.get(rank, int(rank) if rank.isdigit() else 0) for rank in player_ranks]
    player_total = sum(player_values)

    # **Soft Hands (Contains an Ace as 11)**
    if "A" in player_ranks and sum(player_values) <= 21:  # Ensure soft hand check
        if player_total >= 19:  # FIX: Always stand on soft 19 or higher
            return "stand"
        elif player_total == 18:
            return "stand" if dealer_upcard in [2, 7, 8] else "hit"
        elif player_total == 17:
            return "hit"
        else:
            return "hit"

    # **Hard Hands (No Ace or Used as 1)**
    if player_total >= 17:
        return "stand"  # FIX: Always stand on 17+ (hard hands)
    elif 13 <= player_total <= 16:
        return "stand" if 2 <= dealer_upcard <= 6 else "hit"  # FIX: Stand vs. dealer 2-6, hit vs. 7+
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
