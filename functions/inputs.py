def get_valid_input(prompt, valid_inputs):
    """
    Gets valid user input from a list of valid inputs
    :param prompt: Allows for us to create a unique prompt each time this function is needed
    :param valid_inputs: we defined what the valid inputs for that prompt should be
    :return:
    """
    while True: #Repeats
        user_input = input(prompt).strip().lower() #We take the input from the user, strip it and make it lower case to standardise
        if user_input in valid_inputs: #If the input is in the valid inputs that we define then we return the user input
            return user_input #returning the input breaks the while, indicating a proper input from the user allowing the code to then go through
        else:
            print("Invalid input. Please try again.") #Tells user that the input is invalid and since the while input is true will keep repeating

def get_valid_bet(money):
    """
    Gets a valid bet from the user in the form of an integer input
    :param money: Money parameter in the game will represent their balance
    :return:
    """
    while True: #Ensures the while loop keeps running until the break occurs, which will only happen with a valid bet amount being inoputted by user
        try:
            bet = int(input("Place your bet: $")) #Prompts user to enter their bet for the game
            if 0 < bet <= money: #Ensuring that they are entering a positive number within their balance
                return bet #breaks the while, indicating a proper bet being inputted
            else:
                print("Invalid bet amount. Please try again.") #Not a valid number being inputted, loops again to get a proper input
        except ValueError: #Ensure that the input is a valid number, loops again to get a valid input
            print("Invalid input. Please enter a number.")