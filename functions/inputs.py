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

