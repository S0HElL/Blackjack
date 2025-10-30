import random
import os
import time

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_deck():
    """Create a standard 52-card deck."""
    suits = ['♠', '♣', '♥', '♦']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return [f"{rank}{suit}" for suit in suits for rank in ranks]

def evaluate_hand(hand):
    """Calculate the value of a hand."""
    values = {'J': 10, 'Q': 10, 'K': 10}
    hand_value = 0
    aces = 0

    for card in hand:
        rank = card[:-1]  # Remove suit emoji
        if rank == 'A':
            aces += 1
        elif rank in values:
            hand_value += values[rank]
        else:
            hand_value += int(rank)

    # Handle aces
    for _ in range(aces):
        if hand_value + 11 <= 21:
            hand_value += 11
        else:
            hand_value += 1

    return hand_value

def display_hand(name, hand, hide_second=False):
    """Display a player's hand."""
    print(f"\n{name}'s Hand:")
    if hide_second:
        print(f"  {hand[0]}  [Hidden]")
        print(f"  Score: ?")
    else:
        print(f"  {' '.join(hand)}")
        print(f"  Score: {evaluate_hand(hand)}")

def draw_card(deck):
    """Draw a random card from the deck."""
    card = random.choice(deck)
    deck.remove(card)
    return card

def display_game_state(player_hand, dealer_hand, hide_dealer=True):
    """Display the current game state."""
    clear_screen()
    print("=" * 50)
    print("                   BLACKJACK")
    print("=" * 50)
    
    display_hand("Dealer", dealer_hand, hide_dealer)
    display_hand("Player", player_hand)
    print("\n" + "-" * 50)

def player_turn(deck, player_hand, dealer_hand):
    """Handle the player's turn."""
    while True:
        display_game_state(player_hand, dealer_hand, hide_dealer=True)
        
        player_score = evaluate_hand(player_hand)
        
        # Check for bust
        if player_score > 21:
            print("\n💥 BUST! You went over 21!")
            time.sleep(2)
            return False
        
        # Check for 21
        if player_score == 21:
            print("\n🎯 You got 21!")
            time.sleep(2)
            return True
        
        # Get player input
        print("\nChoose an action:")
        print("  [H] Hit - Draw another card")
        print("  [S] Stand - Keep your current hand")
        
        choice = input("\nYour choice: ").strip().upper()
        
        if choice == 'H':
            player_hand.append(draw_card(deck))
        elif choice == 'S':
            return True
        else:
            print("\n❌ Invalid choice! Please enter H or S.")
            time.sleep(1.5)

def dealer_turn(deck, dealer_hand):
    """Handle the dealer's turn."""
    while evaluate_hand(dealer_hand) < 17:
        print(f"\nDealer draws a card...")
        time.sleep(1.5)
        dealer_hand.append(draw_card(deck))
        dealer_score = evaluate_hand(dealer_hand)
        print(f"Dealer's new card: {dealer_hand[-1]}")
        print(f"Dealer's score: {dealer_score}")
        time.sleep(1.5)
        
        if dealer_score > 21:
            print("\n💥 Dealer BUSTS!")
            time.sleep(2)
            return False
    
    return True

def determine_winner(player_hand, dealer_hand):
    """Determine the winner and display results."""
    player_score = evaluate_hand(player_hand)
    dealer_score = evaluate_hand(dealer_hand)
    
    display_game_state(player_hand, dealer_hand, hide_dealer=False)
    
    print("\n" + "=" * 50)
    print("                 FINAL RESULTS")
    print("=" * 50)
    print(f"  Your score:   {player_score}")
    print(f"  Dealer score: {dealer_score}")
    print("-" * 50)
    
    if dealer_score > 21:
        print("\n🎉 YOU WIN! Dealer busted!")
    elif player_score > dealer_score:
        print("\n🎉 YOU WIN! Higher score!")
    elif player_score < dealer_score:
        print("\n😔 DEALER WINS! Dealer has higher score!")
    else:
        print("\n🤝 IT'S A TIE! Push!")
    
    print("=" * 50)

def play_game():
    """Main game loop."""
    # Initialize deck and hands
    deck = initialize_deck()
    player_hand = []
    dealer_hand = []
    
    # Deal initial cards
    for _ in range(2):
        player_hand.append(draw_card(deck))
        dealer_hand.append(draw_card(deck))
    
    # Check for natural blackjack
    player_score = evaluate_hand(player_hand)
    dealer_score = evaluate_hand(dealer_hand)
    
    display_game_state(player_hand, dealer_hand, hide_dealer=True)
    
    if player_score == 21 and dealer_score == 21:
        display_game_state(player_hand, dealer_hand, hide_dealer=False)
        print("\n🤝 Both have BLACKJACK! It's a tie!")
        time.sleep(3)
        return
    elif player_score == 21:
        display_game_state(player_hand, dealer_hand, hide_dealer=False)
        print("\n🎉 BLACKJACK! You win!")
        time.sleep(3)
        return
    elif dealer_score == 21:
        display_game_state(player_hand, dealer_hand, hide_dealer=False)
        print("\n😔 Dealer has BLACKJACK! Dealer wins!")
        time.sleep(3)
        return
    
    # Player's turn
    if not player_turn(deck, player_hand, dealer_hand):
        display_game_state(player_hand, dealer_hand, hide_dealer=False)
        print("\n😔 DEALER WINS!")
        time.sleep(3)
        return
    
    # Dealer's turn
    display_game_state(player_hand, dealer_hand, hide_dealer=False)
    print("\nDealer's turn...")
    time.sleep(2)
    
    dealer_turn(deck, dealer_hand)
    
    # Determine winner
    determine_winner(player_hand, dealer_hand)
    time.sleep(3)

def main():
    """Main program entry point."""
    while True:
        clear_screen()
        print("=" * 50)
        print("                   BLACKJACK")
        print("=" * 50)
        print("\nWelcome to Blackjack!")
        print("\nRules:")
        print("  • Get as close to 21 as possible without going over")
        print("  • Face cards (J, Q, K) are worth 10 points")
        print("  • Aces can be worth 1 or 11 points")
        print("  • Dealer must draw until reaching at least 17")
        print("\n" + "=" * 50)
        
        input("\nPress ENTER to start the game...")
        
        play_game()
        
        # Ask to play again
        while True:
            play_again = input("\nPlay again? (Y/N): ").strip().upper()
            if play_again in ['Y', 'N']:
                break
            print("Please enter Y or N.")
        
        if play_again == 'N':
            clear_screen()
            print("\n" + "=" * 50)
            print("          Thanks for playing Blackjack!")
            print("=" * 50 + "\n")
            break

if __name__ == "__main__":
    main()
    