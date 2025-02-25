try:
    from functions.inputs import *
    from functions.count import *
    from functions.deckgen import *
except ModuleNotFoundError:
    print("Module(s) not found")

print("\nWelcome to Blackjack!")
def blackjack_game():
    """
    Main function to run the Blackjack game along with the card-counting function
    :return:
    """
    money = 1000 #Every player starts with $1000 in their balance
    count = 0 #Ofcourse, the count starts at 0 at the start of the game
    deck = create_deck() #Runs the create_deck function, to create a new shuffled deck at the beginning of every game.
    stop = False

    while (money > 0) and (stop == False): #The game should only run while
        print(f"\nYou have ${money}.")
        bet = get_valid_bet(money)
        print("\nGood luck!")

        player_hand, dealer_hand = deal_initial_cards(deck)
        count = update_count(player_hand, count)
        count = update_count(dealer_hand, count)

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


        stopInput = get_valid_input("Do you want to keep going? (Y)es or (N)o", ['y','n'])
        if stopInput == 'y':
            stop = False
            print("Great! Your not a quitter!")
        elif stopInput == 'n':
            stop = True
            print(f"Thanks for playing! You ended with ${money}")

        if money <= 0:
            print("You're out of money! Game over.")
            break


# Run the game
if __name__ == "__main__":
    blackjack_game()
