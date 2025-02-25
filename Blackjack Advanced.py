import sys
import os
import datetime

# Add the 'functions' folder to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), "functions"))

try:
    from functions.inputs import get_valid_bet, get_valid_input
    from functions.count import calculate_hand_value, update_count
    from functions.deckgen import create_deck, deal_initial_cards, display_hand, format_card
    from functions.perfect_strategy import check_perfect_strategy
except ModuleNotFoundError:
    print("Module(s) not found")

# Define Blackjack Payout Ratio for Natural Blackjack
BLACKJACK_PAYOUT = 3


def blackjack_game():
    """Main function to run a text-based Blackjack game with betting, statistics, and strategy tracking."""
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

        # Format hands with suit emojis
        player_hand = [format_card(card) for card in player_hand]
        dealer_hand = [format_card(card) for card in dealer_hand]

        display_hand("Dealer", dealer_hand, hide_first_card=True)
        display_hand("Player", player_hand)

        # Check for natural blackjack
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        if len(player_hand) == 2 and player_value == 21:
            print("Blackjack! You win 3:1 payout!")
            money += bet * BLACKJACK_PAYOUT
            win += 1
            continue

        # Player's turn loop
        player_turn = True
        while player_turn and calculate_hand_value(player_hand) < 21:
            choice = get_valid_input("Do you want to (H)it, (S)tand, or (SP)lit? ", ['h', 's', 'sp'])

            if choice == 'h':  # Player hits
                new_card = deck.pop()
                player_hand.append(format_card(new_card))
                count = update_count([new_card], count)
                display_hand("Player", player_hand)
                hit += 1
                strategy_correct = check_perfect_strategy(player_hand, dealer_hand)
                print("PS ✔" if strategy_correct else "PS ❌")
            elif choice == 's':  # Player stands
                stand += 1
                player_turn = False
                strategy_correct = check_perfect_strategy(player_hand, dealer_hand)
                print("PS ✔" if strategy_correct else "PS ❌")
            elif choice == 'sp' and player_hand[0].split()[0] == player_hand[1].split()[0]:  # Player splits
                split_count += 1
                print("You chose to split!")
                hand1 = [format_card(player_hand[0]), format_card(deck.pop())]
                hand2 = [format_card(player_hand[1]), format_card(deck.pop())]
                print("Hand 1:")
                display_hand("Player", hand1)
                print("Hand 2:")
                display_hand("Player", hand2)
                strategy_correct = check_perfect_strategy(player_hand, dealer_hand, split=True)
                print("PS ✔" if strategy_correct else "PS ❌")

        # Log game history
        history.append(
            f"{money:<7} stood on {player_value} vs {dealer_value}, count = {count:<3} {'WON ✔' if player_value > dealer_value else 'LOST ❌'}")

        # Ask player if they want to continue
        stop_input = get_valid_input("Do you want to keep going? (Y)es or (N)o", ['y', 'n'])
        if stop_input == 'n':
            stop = True
            print(f"Thanks for playing! You ended with ${money}")
            break

    # Write statistics to file
    with open("game_summary.txt", "a") as file:
        file.write(f"\nGame Summary ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        file.write(f"Max Bet: ${max(bets)}\nMin Bet: ${min(bets)}\n")
        file.write(f"Avg Bet: ${sum(bets) / len(bets) if bets else 0:.2f}\n")
        file.write(f"Win Rate: {win / (win + loss) * 100 if (win + loss) else 0:.2f}%\n")
        file.write(f"Hit Rate: {hit / (hit + stand) * 100 if (hit + stand) else 0:.2f}%\n")
        file.write(f"Splits: {split_count}\n\n")
        file.write("History:\n")
        file.write("\n".join(history))


if __name__ == "__main__":
    blackjack_game()
