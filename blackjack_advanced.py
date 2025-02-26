import sys # import basics
import os
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "functions")) # Redundancy 'functions' folder added to the system path

try: # importing redundantly
    from functions.inputs import get_valid_bet, get_valid_input
    from functions.count import calculate_hand_value, update_count
    from functions.deckgen import create_deck, deal_initial_cards, display_hand, format_card
    from functions.basic_strategy import check_basic_strategy
except ModuleNotFoundError:
    print("Module(s) not found")

BLACKJACK_PAYOUT = 3 # Define Blackjack Payout Ratio for Natural Blackjack


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

        games += 1

        player_hand, dealer_hand = deal_initial_cards(deck)  # Deal initial cards
        count = update_count(player_hand, count)  # Update count with player cards
        count = update_count(dealer_hand, count)  # Update count with dealer cards

        player_hand = [format_card(card) for card in player_hand] # Format hands with suit emojis
        dealer_hand = [format_card(card) for card in dealer_hand] # Format hands with suit emojis

        display_hand("Dealer", dealer_hand, hide_first_card=True) # hide the dealers second card
        display_hand("Player", player_hand)

        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        if len(player_hand) == 2 and player_value == 21:  #Check for natural blackjack
            print("Blackjack! You win 3:1 payout!")
            money += bet * BLACKJACK_PAYOUT
            win += 1
        else:
            original_dealer_upcard = dealer_hand[0].split()[0] if " " in dealer_hand[0] else dealer_hand[0]
            player_turn = True # Player's turn loop
            while player_turn and calculate_hand_value(player_hand) < 21:
                choice = get_valid_input("Do you want to (H)it or (S)tand", ['h', 's'])

                if choice == 'h':  # Player hits
                    new_card = deck.pop()
                    player_hand.append(format_card(new_card))
                    count = update_count([new_card], count)
                    display_hand("Player", player_hand)
                    hit += 1
                    if calculate_hand_value(player_hand) > 21:
                        # Ensure BS check happens before bust message
                        expected_move = check_basic_strategy(player_hand, original_dealer_upcard)  # Pass as string
                        correct_move = expected_move == "hit"  # Since the player hit before busting
                        # Print and record BS check
                        print("BS ✔" if correct_move else "BS ❌")
                        history.append(
                            f"Move: Hit, Player Total: {calculate_hand_value(player_hand)}, "
                            f"Dealer Upcard: {original_dealer_upcard}, Expected Move: {expected_move}, BS {'✔' if correct_move else '❌'}"
                        )
                        # Bust handling
                        print("Bust! You lose.")
                        money -= bet
                        loss += 1
                        player_turn = False

                        guessed_count = int(get_valid_input("What is the current card count? ", [str(i) for i in range(-20,21)]))  # Ask for the current count after each round
                        if guessed_count == count:
                            print("Correct!")
                            correct += 1
                        else:
                            print(f"Incorrect. The correct count is {count}.")

                        stop_input = get_valid_input("Do you want to keep going? (Y)es or (N)o",
                                                     ['y', 'n'])  # Ask player if they want to continue
                        if stop_input == 'n':
                            stop = True
                            print(f"Thanks for playing! You ended with ${money}")
                            break
                        correct_strategy = sum(1 for move in history if "BS ✔" in move) # Track correct strategy decisions
                        total_strategy_checks = sum(1 for move in history if "BS" in move)
                        strategy_accuracy = (correct_strategy / total_strategy_checks * 100) if total_strategy_checks > 0 else 100

                        with open("game_summary.txt", "a",
                                  encoding="utf-8") as file:  # making sure our emojis are in the text file with this encoding
                            file.write(f"\nGame Summary ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
                            file.write(f"Final Amount: {money}\n")
                            file.write(
                                f"Wins: {win}; Losses: {loss} (Win Rate: {win / (win + loss) * 100 if (win + loss) else 0:.2f}%)\n")
                            file.write(
                                f"Hits: {hit}; Stands: {stand}; (Hit Rate: {hit / (hit + stand) * 100 if (hit + stand) else 0:.2f}%)\n")
                            file.write(f"Card Counting Accuracy: {correct / (games if games else 1) * 100:.2f}%\n")
                            file.write(f"Basic Strategy Accuracy: {strategy_accuracy:.2f}%\n")  # New line for BS accuracy
                            file.write("\nHistory:\n")
                            file.write("\n".join(history))
                        continue  # Skip dealer's turn if player busts
                    elif calculate_hand_value(player_hand) == 21:
                        player_turn = False  # End player's turn if exactly 21
                    # Ensure expected move is correctly checked based on original dealer upcard
                    expected_move = check_basic_strategy(player_hand, [original_dealer_upcard])
                    # Ensure move is compared correctly
                    correct_move = (choice == 'h' and expected_move == "hit") or (
                                choice == 's' and expected_move == "stand")

                    # Print and record the BS check
                    print("BS ✔" if correct_move else "BS ❌")

                    # Store move history correctly
                    history.append(
                        f"Move: {'Hit' if choice == 'h' else 'Stand'}, Player Total: {calculate_hand_value(player_hand)}, "
                        f"Dealer Upcard: {original_dealer_upcard}, Expected Move: {expected_move}, BS {'✔' if correct_move else '❌'}"
                    )
                if choice == 's':  # Player stands
                    stand += 1  # Increment stand counter
                    expected_move = check_basic_strategy(player_hand,
                                                         [original_dealer_upcard])  # Pass dealer upcard as list
                    expected_move = expected_move.strip().lower()  # Normalize case to prevent mismatches
                    correct_move = expected_move == "stand"  # Ensure correct comparison

                    correct_move = expected_move.strip().lower() == "stand"  # Ensure lowercase match
                    print(f"BS {'✔' if correct_move else '❌'} (Expected: {expected_move}, Your Move: Stand)")

                    # Log move history properly
                    history.append(
                        f"Move: Stand, Player Total: {calculate_hand_value(player_hand)}, "
                        f"Dealer Upcard: {original_dealer_upcard}, Expected Move: {expected_move}, BS {'✔' if correct_move else '❌'}"
                    )
                    player_turn = False  # Ensure turn ends when standing

        if calculate_hand_value(player_hand) > 21: # skip the dealer if you've busted
            continue
        if player_value <= 21:
            print("\nDealer's turn:")
            display_hand("Dealer", dealer_hand)
            while calculate_hand_value(dealer_hand) < 17:
                new_card = deck.pop()
                dealer_hand.append(format_card(new_card))
                count = update_count([new_card], count)
                display_hand("Dealer", dealer_hand)
            dealer_value = calculate_hand_value(dealer_hand)

        player_value = calculate_hand_value(player_hand) # Recalculate player's hand value before determining the winner

        print("\nFinal Results:") # Determine winner
        display_hand("Player", player_hand)
        display_hand("Dealer", dealer_hand)

        if calculate_hand_value(player_hand) > 21:
            expected_move = check_basic_strategy(player_hand, original_dealer_upcard)  # Pass as string
            correct_move = expected_move == "hit"  # Since the player hit before busting
            # Print and record the BS check
            print("BS ✔" if correct_move else "BS ❌")
            history.append(
                f"Move: Hit, Player Total: {calculate_hand_value(player_hand)}, "
                f"Dealer Upcard: {original_dealer_upcard}, Expected Move: {expected_move}, BS {'✔' if correct_move else '❌'}"
            )
            # Bust handling
            print("Bust! You lose.")
            money -= bet
            loss += 1
            player_turn = False
        elif dealer_value > 21 or player_value > dealer_value:
            print("You win!")
            money += bet
            win += 1
        elif dealer_value == player_value:
            print("It's a tie!")
        else:
            print("Dealer wins!")
            money -= bet
            loss += 1

            result = "WON ✔(Dealer Bust)" if dealer_value > 21 else "WON ✔" if player_value > dealer_value else "LOST ❌(Player Bust)" if player_value > 21 else "LOST ❌" if dealer_value > player_value else "TIE"
            strategy_correct = check_basic_strategy(player_hand, dealer_hand)
            history.append(
            f"{money}    stood on {player_value} vs {dealer_value}, count = {count}       {result}, BS {'✔' if strategy_correct else '❌'}") # recording of the results into the list

        guessed_count = int(get_valid_input("What is the current card count? ", [str(i) for i in range(-20, 21)]))  # Ask for the current count after each round
        if guessed_count == count:
            print("Correct!")
            correct += 1
        else:
            print(f"Incorrect. The correct count is {count}.")

        stop_input = get_valid_input("Do you want to keep going? (Y)es or (N)o", ['y', 'n']) # Ask player if they want to continue
        if stop_input == 'n':
            stop = True
            print(f"Thanks for playing! You ended with ${money}")
            break
    # Track correct strategy decisions
    correct_strategy = sum(1 for move in history if "BS ✔" in move)
    total_strategy_checks = sum(1 for move in history if "BS" in move)
    strategy_accuracy = (correct_strategy / total_strategy_checks * 100) if total_strategy_checks > 0 else 100

    # Write statistics to file
    with open("game_summary.txt", "a", encoding="utf-8") as file: # making sure our emojis are in the text file with this encoding
        file.write(f"\nGame Summary ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        file.write(f"Final Amount: {money}\n")
        file.write(f"Wins: {win}; Losses: {loss} (Win Rate: {win / (win + loss) * 100 if (win + loss) else 0:.2f}%)\n")
        file.write(
            f"Hits: {hit}; Stands: {stand}; (Hit Rate: {hit / (hit + stand) * 100 if (hit + stand) else 0:.2f}%)\n")
        file.write(f"Card Counting Accuracy: {correct / (games if games else 1) * 100:.2f}%\n")
        file.write(f"Basic Strategy Accuracy: {strategy_accuracy:.2f}%\n")  # New line for BS accuracy
        file.write("\nHistory:\n")
        file.write("\n".join(history))

if __name__ == "__main__":
    blackjack_game()
