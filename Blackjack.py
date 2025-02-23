import random

# Define the deck with card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Card counting system values
counting_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1,
    'J': -1, 'Q': -1, 'K': -1, 'A': -1
}


def create_deck():
    """Creates a deck consisting of 6 standard 52-card decks."""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [f"{rank} of {suit}" for suit in suits for rank in card_values.keys()] * 6
    random.shuffle(deck)
    return deck


def calculate_hand_value(hand):
    """Calculates the value of a hand, handling Aces properly."""
    value = sum(card_values[card.split()[0]] for card in hand)
    ace_count = sum(1 for card in hand if card.startswith('A'))
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1
    return value


def deal_initial_cards(deck):
    """Deals two cards to both the player and dealer."""
    return [deck.pop(), deck.pop()], [deck.pop(), deck.pop()]


def display_hand(player, hand, hide_first_card=False):
    """Displays a player's hand."""
    if hide_first_card:
        print(f"{player}'s hand: [Hidden], {hand[1]}")
    else:
        print(f"{player}'s hand: {', '.join(hand)} (Value: {calculate_hand_value(hand)})")


def update_count(hand, count):
    """Updates the card count based on the dealt hand."""
    for card in hand:
        rank = card.split()[0]
        count += counting_values[rank]
    return count


def get_valid_input(prompt, valid_inputs):
    """Gets valid user input from a list of valid inputs."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_inputs:
            return user_input
        print("Invalid input. Please try again.")


def get_valid_bet(money):
    """Gets a valid bet from the user."""
    while True:
        try:
            bet = int(input("Place your bet: $"))
            if 0 < bet <= money:
                return bet
            print("Invalid bet amount. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


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
