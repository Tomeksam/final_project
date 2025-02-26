def check_perfect_strategy(player_hand, dealer_hand, split=False):
    """
    Checks if the player's move aligns with basic blackjack strategy.
    Covers hard hands, soft hands, and splitting rules.

    :Parameters:
        player_hand (list of str): List of player's card strings with emoji suits.
        dealer_hand (list of str): List of dealer's card strings with emoji suits.
        split (bool): True if the player has split their hand, otherwise False.

    Returns:
        bool: True if the move follows perfect strategy, False otherwise.
    """

    # Mapping face cards and Aces
    card_values = {"J": 10, "Q": 10, "K": 10, "A": 11}

    # Extract dealer's upcard rank and remove suit emoji
    dealer_upcard = dealer_hand[0][:-1]
    dealer_upcard = card_values.get(dealer_upcard, int(dealer_upcard) if dealer_upcard.isdigit() else 0)

    # Extract player's hand ranks and convert values
    player_ranks = [card[:-1] for card in player_hand]
    player_values = [card_values.get(rank, int(rank) if rank.isdigit() else 0) for rank in player_ranks]
    player_total = sum(player_values)

    # Check for splitting conditions
    if split or (len(player_hand) == 2 and player_ranks[0] == player_ranks[1]):
        pair_rank = player_ranks[0]
        if pair_rank in ["A", "8"]:
            return True  # Always split Aces and 8s
        elif pair_rank == "10":
            return False  # Never split 10s
        elif pair_rank == "9":
            return dealer_upcard not in [7, 10, 11]  # Split unless against 7, 10, A
        elif pair_rank == "7":
            return dealer_upcard < 8  # Split vs 2-7
        elif pair_rank == "6":
            return dealer_upcard < 7  # Split vs 2-6
        elif pair_rank == "4":
            return dealer_upcard in [5, 6]  # Split vs 5-6
        elif pair_rank in ["3", "2"]:
            return dealer_upcard < 8  # Split vs 2-7
        else:
            return False  # Default case (not a split situation)

    # Check for soft hand (Ace involved and only two cards)
    if "A" in player_ranks and len(player_hand) == 2:
        if player_total == 18:
            return dealer_upcard in [2, 7, 8]  # Stand vs 2, 7, 8; otherwise hit
        elif player_total >= 19:
            return True  # Always stand on 19+
        else:
            return False  # Hit on soft totals 13-17

    # Basic Strategy Conditions for Hard Hands
    if player_total >= 17:
        return True  # Always stand on 17+
    elif 13 <= player_total <= 16:
        return dealer_upcard < 7  # Stand on 13-16 if dealer shows 2-6, otherwise hit
    elif player_total == 12:
        return dealer_upcard in [4, 5, 6]  # Stand on 12 if dealer shows 4-6, otherwise hit
    elif player_total == 11:
        return True  # Always hit on 11
    elif player_total == 10:
        return dealer_upcard < 10  # Hit if dealer has 10 or A
    elif player_total == 9:
        return dealer_upcard in [3, 4, 5, 6]  # Hit unless dealer shows 3-6
    else:
        return False  # Always hit on anything below 9