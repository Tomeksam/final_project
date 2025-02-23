try:
    from functions.inputs import *
    from functions.count import *
    from functions.deckgen import *
except ModuleNotFoundError:
    print("Module(s) not found")

def blackjack_game():
    """Main function to run a text-based Blackjack game with betting and card counting."""
    money = 1000
    count = 0
    deck = create_deck()

    while money > 0:
        print(f"\nYou have ${money}.")
        bet = get_valid_bet(money)

        player_hand, dealer_hand = deal_initial_cards(deck)
        count = update_count(player_hand, count)
        count = update_count(dealer_hand, count)

        print("\nWelcome to Blackjack!")
        display_hand("Dealer", dealer_hand, hide_first_card=True)
        display_hand("Player", player_hand)

        # Player's turn
        while calculate_hand_value(player_hand) < 21:
            choice = get_valid_input("Do you want to (H)it or (S)tand? ", ['h', 's'])
            if choice == 'h':
                player_hand.append(deck.pop())
                count = update_count([player_hand[-1]], count)
                display_hand("Player", player_hand)
            elif choice == 's':
                break

        player_value = calculate_hand_value(player_hand)
        if player_value > 21:
            print("Bust! You lose.")
            money -= bet
        else:
            # Dealer's turn
            print("\nDealer's turn:")
            display_hand("Dealer", dealer_hand)
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                count = update_count([dealer_hand[-1]], count)
                display_hand("Dealer", dealer_hand)

            dealer_value = calculate_hand_value(dealer_hand)

            # Determine the winner
            print("\nFinal Results:")
            display_hand("Player", player_hand)
            display_hand("Dealer", dealer_hand)

            if dealer_value > 21 or player_value > dealer_value:
                print("You win!")
                money += bet
            elif dealer_value == player_value:
                print("It's a tie!")
            else:
                print("Dealer wins!")
                money -= bet

        # Ask for card count after each round
        try:
            guessed_count = int(input("What is the current card count? "))
            if guessed_count == count:
                print("Correct!")
            else:
                print(f"Incorrect. The correct count is {count}.")
        except ValueError:
            print(f"Invalid input. The correct count is {count}.")

        if money <= 0:
            print("You're out of money! Game over.")
            break


# Run the game
if __name__ == "__main__":
    blackjack_game()
