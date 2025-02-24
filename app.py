from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

def initialize_deck():
    cardsuits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
    cardtypes = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    return [f"{card} of {suit}" for suit in cardsuits for card in cardtypes]

def evaluate_hand(hand):
    values = {'J': 10, 'Q': 10, 'K': 10}
    hand_value = 0
    aces = 0

    for card in hand:
        rank = card.split()[0]
        if rank == 'A':
            aces += 1
        elif rank in values:
            hand_value += values[rank]
        else:
            hand_value += int(rank)

    for _ in range(aces):
        if hand_value + 11 <= 21:
            hand_value += 11
        else:
            hand_value += 1

    return hand_value

def card_to_image(card):
    """Converts a card name (e.g., '5 of Diamonds') to an image filename (e.g., 'd5.jpg')."""
    rank, suit = card.split(' of ')
    suit_map = {'Spades': 's', 'Clubs': 'c', 'Hearts': 'h', 'Diamonds': 'd'}
    rank_map = {'A': 'a', 'J': 'j', 'Q': 'q', 'K': 'k'}
    
    # Convert rank to lowercase and handle face cards
    rank = rank_map.get(rank, rank.lower())
    
    # Convert suit to lowercase and map to single letter
    suit = suit_map.get(suit, suit[0].lower())
    
    return f"{suit}{rank}.jpg"

@app.route('/')
def index():
    if 'deck' not in session:
        session['deck'] = initialize_deck()
        session['player_hand'] = []
        session['computer_hand'] = []
        session['player_score'] = 0
        session['computer_score'] = 0
        session['game_over'] = False

        # Draw initial hands
        for _ in range(2):
            session['player_hand'].append(random.choice(session['deck']))
            session['deck'].remove(session['player_hand'][-1])
            session['computer_hand'].append(random.choice(session['deck']))
            session['deck'].remove(session['computer_hand'][-1])

        session['player_score'] = evaluate_hand(session['player_hand'])
        session['computer_score'] = evaluate_hand(session['computer_hand'])

        # Check for natural blackjack
        if session['player_score'] == 21:
            session['game_over'] = True
            session['message'] = "Player has a natural Blackjack! Player wins!"
        elif session['computer_score'] == 21:
            session['game_over'] = True
            session['message'] = "Computer has a natural Blackjack! Computer wins!"

    # Convert card names to image paths
    player_images = [card_to_image(card) for card in session['player_hand']]
    
    # Only show the first card of the computer's hand initially
    if session['game_over']:
        computer_images = [card_to_image(card) for card in session['computer_hand']]
    else:
        computer_images = [card_to_image(session['computer_hand'][0]), "back.jpg"]

    return render_template('index.html', player_images=player_images, computer_images=computer_images)

@app.route('/hit', methods=['POST'])
def hit():
    if not session['game_over']:
        session['player_hand'].append(random.choice(session['deck']))
        session['deck'].remove(session['player_hand'][-1])
        session['player_score'] = evaluate_hand(session['player_hand'])

        if session['player_score'] > 21:
            session['game_over'] = True
            session['message'] = "You busted! Computer wins."
        elif session['player_score'] == 21:
            session['game_over'] = True
            session['message'] = "Player got 21! Player wins!"

    return redirect(url_for('index'))

@app.route('/stand', methods=['POST'])
def stand():
    if not session['game_over']:
        # Computer draws one card at a time until its score is at least 17
        while session['computer_score'] < 17:
            session['computer_hand'].append(random.choice(session['deck']))
            session['deck'].remove(session['computer_hand'][-1])
            session['computer_score'] = evaluate_hand(session['computer_hand'])

            # Check if computer busts after drawing a card
            if session['computer_score'] > 21:
                session['game_over'] = True
                session['message'] = "Computer busted! Player wins!"
                break

        # If the computer didn't bust, determine the winner
        if not session['game_over']:
            if session['player_score'] > session['computer_score']:
                session['message'] = "Player wins!"
            elif session['player_score'] < session['computer_score']:
                session['message'] = "Computer wins!"
            else:
                session['message'] = "It's a tie!"
            session['game_over'] = True

    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)