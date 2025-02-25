import sys
import os

# Add the 'functions' folder to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), "functions"))

try:
    from functions.inputs import get_valid_bet, get_valid_input
    from functions.count import calculate_hand_value, update_count
    from functions.deckgen import create_deck, deal_initial_cards, display_hand
    from functions.perfect_strategy import check_perfect_strategy
    import datetime
except ModuleNotFoundError:
    print("Module(s) not found")

# Define Blackjack Payout Ratio for Natural Blackjack
BLACKJACK_PAYOUT = 3

def blackjack_game():
    """Main function to run a text-based Blackjack game with betting, statistics, and strategy tracking.

    The game follows traditional Blackjack rules, including hitting, standing, splitting, and dealer logic.
    It tracks various statistics, evaluates player decisions against a perfect strategy, and writes a game summary.
    """
    money = 1000  # Starting money
    count = 0  # Running card count
    deck = create_deck()  # Generate shuffled deck
    stop = False  # Control loop termination
    win, loss, games, correct, hit, stand, split_count = 0, 0, 0, 0, 0, 0, 0  # Initialize statistics
    bets = []  # Track bet values for statistics
    history = []  # Chronological game history

    print("\nWelcome to Blackjack!")
    while money > 0 and not stop:
        print(f"\nYou have ${money}.")
        bet = get_valid_bet(money)  # Get valid bet input
        bets.append(bet)
        print("\nGood luck!")

        # Deal initial cards
        player_hand, dealer_hand = deal_initial_cards(deck)
        count = update_count(player_hand, count)  # Update count with player cards
        count = update_count(dealer_hand, count)  # Update count with dealer cards

        display_hand("Dealer", dealer_hand, hide_first_card=True)
        display_hand("Player", player_hand)

        # Check for natural blackjack
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        if player_value == 21:
            print("Blackjack! You win 3:1 payout!")
            money += bet * BLACKJACK_PAYOUT
            win += 1
            continue

        # Player's turn loop
        player_turn = True
        while player_turn and calculate_hand_value(player_hand) < 21:
            choice = get_valid_input("Do you want to (H)it, (S)tand, or (SP)lit? ", ['h', 's', 'sp'])

            if choice == 'h':  # Player hits
                player_hand.append(deck.pop())
                count = update_count([player_hand[-1]], count)
                display_hand("Player", player_hand)
                hit += 1
                # Check perfect strategy after a hit
                strategy_correct = check_perfect_strategy(player_hand, dealer_hand)
                print("PS ✔" if strategy_correct else "PS ❌")
            elif choice == 's':  # Player stands
                stand += 1
                player_turn = False
                # Check perfect strategy after standing
                strategy_correct = check_perfect_strategy(player_hand, dealer_hand)
                print("PS ✔" if strategy_correct else "PS ❌")
            elif choice == 'sp' and player_hand[0].split()[0] == player_hand[1].split()[0]:  # Player splits
                split_count += 1
                print("You chose to split!")
                hand1 = [player_hand[0], deck.pop()]
                hand2 = [player_hand[1], deck.pop()]
                print("Hand 1:")
                display_hand("Player", hand1)
                print("Hand 2:")
                display_hand("Player", hand2)

                # Check perfect strategy after splitting
                strategy_correct = check_perfect_strategy(player_hand, dealer_hand, split=True)
                print("PS ✔" if strategy_correct else "PS ❌")


if __name__ == "__main__":
    blackjack_game()
