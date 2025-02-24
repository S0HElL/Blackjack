import random
import os
import matplotlib.pyplot as plt

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

    def should_hit(self):
        """Automatically decides whether to hit or stand based on a simple strategy."""
        score = self.evaluate_hand()
        # Simple strategy: hit if score is less than 17
        return score < 17


def play_blackjack(verbose=False):
    """Plays a single round of Blackjack. Set verbose=True to print details."""
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

    if verbose:
        print(f"{player.name}'s Hand: {player.show_hand()}")
        print(f"Score: {player_score}\n")
        print(f"Computer's First Card: [{computer.hand[0]}] (Computer's score hidden)\n")

    # Check if player got natural blackjack (21) at the start
    if player_score == 21:
        if verbose:
            print(f"Player has a natural Blackjack! Player wins!")
            print(f"Final Hand: {player.show_hand()}")
            print(f"Score: {player_score}")
            print(f"Computer's Hand: {computer.show_hand()}")
            print(f"Score: {computer_score}")
        return "Player"  # Player wins

    # Check if computer got natural blackjack (21) at the start
    elif computer_score == 21:
        if verbose:
            print(f"Computer has a natural Blackjack! Computer wins!")
            print(f"Player's Hand: {player.show_hand()}")
            print(f"Score: {player_score}")
            print(f"Final Hand: {computer.show_hand()}")
            print(f"Score: {computer_score}")
        return "Computer"  # Computer wins

    # Player's turn (Automated)
    while player_score < 21:  # Stop the loop if score reaches 21
        if player.should_hit():
            player.hit(deck)  # Add one new card to the hand
            player_score = player.evaluate_hand()  # Re-evaluate the score
            if verbose:
                clear_screen()
                print(f"{player.name}'s Hand: {player.show_hand()}")
                print(f"Score: {player_score}\n")

            if player_score > 21:  # Bust check
                if verbose:
                    print("You busted! Computer wins.")
                    print(f"Final Hand: {player.show_hand()}")
                return "Computer"  # Computer wins

            elif player_score == 21:  # Blackjack check
                if verbose:
                    print("Player got 21! Player wins!")
                return "Player"  # Player wins
        else:
            break  # Stand

    # Computer's turn (Automated: hits if score < 17)
    if player_score <= 21:
        if verbose:
            print(f"Computer's Hand: {computer.show_hand()}")
            print(f"Score: {computer_score}\n")

        while computer_score < 17:
            computer.hit(deck)  # Draw one card for the computer
            computer_score = computer.evaluate_hand()  # Re-evaluate the score
            if verbose:
                clear_screen()
                print(f"Computer hits: {computer.show_hand()}")
                print(f"Score: {computer_score}\n")

            if computer_score > 21:
                if verbose:
                    print("Computer busted! Player wins!")
                return "Player"  # Player wins

    # Determine winner
    if player_score <= 21 and computer_score <= 21:
        if player_score > computer_score:
            if verbose:
                print("Player wins!")
            return "Player"
        elif player_score < computer_score:
            if verbose:
                print("Computer wins!")
            return "Computer"
        else:
            if verbose:
                print("It's a tie!")
            return "Tie"

    # Show final hands and scores (one-time display)
    if verbose:
        print("\nFinal Hands:")
        print(f"{player.name}'s Hand: {player.show_hand()}")
        print(f"Score: {player_score}")
        print(f"Computer's Hand: {computer.show_hand()}")
        print(f"Score: {computer_score}\n")

    return "Tie"  # Fallback in case of unexpected outcomes


# Monte Carlo Simulation
def monte_carlo_simulation(num_simulations=1000):
    """Runs multiple simulations of Blackjack and collects statistics."""
    results = {"Player": 0, "Computer": 0, "Tie": 0}

    for _ in range(num_simulations):
        winner = play_blackjack(verbose=False)  # Run without printing details
        results[winner] += 1

    return results


# Function to plot results
def plot_results(results, chart_type="bar"):
    """Plots the results of the Monte Carlo simulation using matplotlib."""
    labels = list(results.keys())
    values = list(results.values())

    if chart_type == "bar":
        # Bar Chart
        plt.bar(labels, values, color=["blue", "red", "green"])
        plt.title("Blackjack Monte Carlo Simulation Results")
        plt.xlabel("Outcome")
        plt.ylabel("Number of Wins")
        plt.show()

    elif chart_type == "pie":
        # Pie Chart
        plt.pie(values, labels=labels, autopct="%1.1f%%", colors=["blue", "red", "green"])
        plt.title("Blackjack Monte Carlo Simulation Results")
        plt.show()

    else:
        print("Invalid chart type. Choose 'bar' or 'pie'.")


# Main function to run the simulation and plot results
if __name__ == "__main__":
    # Run simulation
    num_simulations = 1000
    results = monte_carlo_simulation(num_simulations)

    # Print results
    print(f"Results after {num_simulations} simulations:")
    print(f"Player wins: {results['Player']}")
    print(f"Computer wins: {results['Computer']}")
    print(f"Ties: {results['Tie']}")

    # Plot results
    plot_results(results, chart_type="bar")  # Change to "pie" for a pie chart