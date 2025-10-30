# Blackjack Game

A web-based Blackjack game built with Flask, featuring a sleek dark theme and intuitive gameplay.

## Features

- Classic Blackjack gameplay - Play against the computer dealer
- Visual card display - Card images with emoji labels for easy identification
- Real-time scoring - Track your score and the dealer's score
- Responsive design - Clean, modern interface with smooth animations
- Session management - Game state persists during your session

## Game Rules

- Get as close to 21 as possible without going over
- Face cards (J, Q, K) are worth 10 points
- Aces can be worth 1 or 11 points
- **Hit**: Draw another card
- **Stand**: Keep your current hand and let the dealer play
- Dealer must draw cards until reaching at least 17
- Bust (go over 21) and you lose automatically

## Installation

### Prerequisites

- Python 3.7 or higher
- Git (optional, for cloning)

### Setup Instructions

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd blackjack-game
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **On Windows (Git Bash):**
   ```bash
   source venv/Scripts/activate
   ```
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install flask
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   
   Navigate to: `http://127.0.0.1:5000`

## Project Structure

```
blackjack-game/
│
├── app.py                          # Main Flask application
├── templates/
│   └── index.html                  # HTML template
├── static/
│   ├── styles.css                  # CSS styling
│   └── assets/
│       └── images/                 # Card images
│           ├── sa.png              # Ace of Spades
│           ├── h2.png              # 2 of Hearts
│           ├── back.png            # Card back
│           └── ...                 # Other card images
└── README.md                       # This file
```

## Card Image Naming Convention

Card images should follow this naming pattern:
- **Format**: `{suit}{rank}.png`
- **Suits**: `s` (Spades), `h` (Hearts), `d` (Diamonds), `c` (Clubs)
- **Ranks**: `a` (Ace), `2-10`, `j` (Jack), `q` (Queen), `k` (King)

**Examples:**
- `sa.png` - Ace of Spades (A♠)
- `h5.png` - 5 of Hearts (5♥)
- `dk.png` - King of Diamonds (K♦)
- `back.png` - Card back (for hidden cards)

**Note:** Card emoji labels are displayed below each card image, so missing images won't prevent gameplay.

## Configuration

### Changing the Secret Key

For security, update the secret key in `app.py`:

```python
app.secret_key = 'your_secure_secret_key_here'
```

Generate a secure secret key using:
```python
import secrets
print(secrets.token_hex(16))
```

### Debug Mode

Debug mode is enabled by default. For production, change in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=False)
```

## How to Play

1. **Start the game** - Cards are automatically dealt when you load the page
2. **Review your hand** - Check your cards and score
3. **Make your move**:
   - Click **Hit** to draw another card
   - Click **Stand** to keep your hand and let the dealer play
4. **Win conditions**:
   - Get closer to 21 than the dealer without busting
   - Dealer busts and you don't
   - Get a natural Blackjack (21 with first two cards)
5. **Play again** - Click "Play Again" to start a new game

## Troubleshooting

### Images not loading
- Ensure card images are in `/static/assets/images/` directory
- Check that image filenames match the naming convention
- Card labels with emojis will still display if images are missing

### Port already in use
- Change the port in `app.py`:
  ```python
  app.run(debug=True, port=5001)
  ```

### Session issues
- Clear your browser cookies for localhost
- Make sure the secret key is set in `app.py`

## Future Enhancements

- Add betting system with chips
- Implement split and double down options
- Add sound effects
- Track win/loss statistics
- Multiplayer support
- Mobile-responsive improvements

## License

This project is open source and available under the MIT License.

## Contributing

Contributions, issues, and feature requests are welcome!

## Author

Created for Blackjack enthusiasts