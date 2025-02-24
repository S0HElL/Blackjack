import random
import os  # For clearing the screen

def clear_screen():
    """Clears the console screen (works for Windows & Mac/Linux)."""
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_hand(self, deck):
        """Draws two random cards from the deck and removes them from the deck."""
        for _ in range(2):
            card = random.choice(deck)
            self.hand.append(card)
            deck.remove(card)

    def hit(self, deck):
        """Draws one more card when the player chooses to hit and removes it from the deck."""
        card = random.choice(deck)
        self.hand.append(card)  # Append only one new card to the hand
        deck.remove(card)  # Ensure the card is removed from the deck

    def show_hand(self):
        """Displays the player's hand inside brackets."""
        return f"[{', '.join(self.hand)}]"

    def evaluate_hand(self):
        """Evaluates the hand based on Blackjack rules (Aces can be 1 or 11)."""
        values = {'J': 10, 'Q': 10, 'K': 10}  # Face cards mapped
        hand_value = 0
        aces = 0

        for card in self.hand:
            rank = card.split()[0]  # Extract rank (e.g., 'A', '10', 'K')

            if rank == 'A':
                aces += 1
            elif rank in values:
                hand_value += values[rank]
            else:
                hand_value += int(rank)  # Convert numbered cards

        # Add Aces as 11, but if that causes a bust, treat them as 1
        for _ in range(aces):
            if hand_value + 11 <= 21:
                hand_value += 11
            else:
                hand_value += 1

        return hand_value


def play_blackjack():
    while True:
        clear_screen()

        # Initialize deck
        cardsuits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        cardtypes = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        deck = [f"{card} of {suit}" for suit in cardsuits for card in cardtypes]

        # Create player and computer
        player = Player("Player")
        computer = Player("Computer")

        # Assign hands
        player.draw_hand(deck)
        computer.draw_hand(deck)

        # Evaluate initial hands
        player_score = player.evaluate_hand()
        computer_score = computer.evaluate_hand()

        # Show initial hands
        print(f"{player.name}'s Hand: {player.show_hand()}")
        print(f"Score: {player_score}\n")
        print(f"Computer's First Card: [{computer.hand[0]}] (Computer's score hidden)\n")

        # Check if player got natural blackjack (21) at the start
        if player_score == 21:
            print(f"Player has a natural Blackjack! Player wins!")
            print(f"Final Hand: {player.show_hand()}")
            print(f"Score: {player_score}")
            print(f"Computer's Hand: {computer.show_hand()}")
            print(f"Score: {computer_score}")
            continue  # Go to next round

        # Check if computer got natural blackjack (21) at the start
        elif computer_score == 21:
            print(f"Computer has a natural Blackjack! Computer wins!")
            print(f"Player's Hand: {player.show_hand()}")
            print(f"Score: {player_score}")
            print(f"Final Hand: {computer.show_hand()}")
            print(f"Score: {computer_score}")
            continue  # Go to next round

        # Player's turn (Hit or Stand)
        while player_score < 21:  # Stop the loop if score reaches 21
            choice = input("Enter 1 to Hit or 2 to Stand: ")

            if choice == '1':  # Hit
                player.hit(deck)  # Add one new card to the hand
                player_score = player.evaluate_hand()  # Re-evaluate the score
                clear_screen()
                print(f"{player.name}'s Hand: {player.show_hand()}")
                print(f"Score: {player_score}\n")

                if player_score > 21:  # Bust check
                    print("You busted! Computer wins.")
                    print(f"Final Hand: {player.show_hand()}")
                    break  # End the game immediately if bust

                elif player_score == 21:  # Blackjack check
                    print("Player got 21! Player wins!")
                    break  # End the game if player hits 21

            elif choice == '2':  # Stand
                break

        if player_score > 21:
            # Show final hands and scores (one-time display)
            print("\nFinal Hands:")
            print(f"{player.name}'s Hand: {player.show_hand()}")
            print(f"Score: {player_score}")
            print(f"Computer's Hand: {computer.show_hand()}")
            print(f"Score: {computer_score}\n")

            # Ask to play again
            again = input("\nPlay again? (y/n): ").strip().lower()
            if again == 'n':
                print("Thanks for playing! Goodbye!")
                break
            else:
                continue  # Go to next round

        # Computer's turn (Automated: hits if score < 17)
        if player_score <= 21:
            print(f"Computer's Hand: {computer.show_hand()}")
            print(f"Score: {computer_score}\n")

            while computer_score < 17:
                computer.hit(deck)  # Draw one card for the computer
                computer_score = computer.evaluate_hand()  # Re-evaluate the score
                clear_screen()
                print(f"Computer hits: {computer.show_hand()}")
                print(f"Score: {computer_score}\n")

                if computer_score > 21:
                    print("Computer busted! Player wins!")
                    break  # End the game immediately if computer busts

        # Determine winner
        if player_score <= 21 and computer_score <= 21:
            if player_score > computer_score:
                print("Player wins!")
            elif player_score < computer_score:
                print("Computer wins!")
            else:
                print("It's a tie!")

        # Show final hands and scores (one-time display)
        print("\nFinal Hands:")
        print(f"{player.name}'s Hand: {player.show_hand()}")
        print(f"Score: {player_score}")
        print(f"Computer's Hand: {computer.show_hand()}")
        print(f"Score: {computer_score}\n")

        # Ask to play again
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again == 'n':
            print("Thanks for playing! Goodbye!")
            break

# Start the game
play_blackjack()