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
    win = 0
    loss = 0
    correct = 0
    games = 0
    hit = 0
    stand = 0

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
                hit += 1
            elif choice == 's':
                stand += 1
                break


        player_value = calculate_hand_value(player_hand)
        if player_value > 21:
            print("Bust! You lose.")
            money -= bet
            loss += 1
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
                win += 1
            elif dealer_value == player_value:
                print("It's a tie!")
            else:
                print("Dealer wins!")
                money -= bet
                loss += 1

        # Ask for card count after each round
        try:
            guessed_count = int(input("What is the current card count? "))
            if guessed_count == count:
                print("Correct!")
                correct += 1
            else:
                print(f"Incorrect. The correct count is {count}.")
        except ValueError:
            print(f"Invalid input. The correct count is {count}.")


        stopinput = get_valid_input("Do you want to cash out? (Y)es or (N)o", ['y','n'])
        if stopinput == 'n':
            print("Great! Your not a quitter!")
            games += 1
        elif stopInput == 'n':
            print(f"Thanks for playing! You ended with ${money}")
            with open("game_summary.txt", "a") as fp: # a - append; add to this file or create it if it doesn't exist
                fp.write(f"\n\nGame: {datetime.datetime.now()} \nFinal Amount: {money}\n Wins: {win}; Losses: {loss}\n Hits: {hit}; Stands: {stand}\n Card Counting Accuracy: {correct/games}%") # this is the same as the line below
            # fp.write(text + "\n")
            break
        if money <= 0:
            print("You're out of money! Game over.")
            with open("game_summary.txt", "a") as fp: # a - append; add to this file or create it if it doesn't exist
                fp.write(f"\n\nGame: {datetime} \nFinal Amount: {money}\n Wins: {win}; Losses: {loss}\n Hits: {hit}; Stands: {stand}\n Card Counting Accuracy: {(correct/games)*100}%") # this is the same as the line below
            # fp.write(text + "\n")
            break

# Run the game
if __name__ == "__main__":
    blackjack_game()
