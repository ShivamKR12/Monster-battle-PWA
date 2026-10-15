# Monster Battle (Progressive Web App (PWA))

A turn-based monster battle game built with Python and Pygame-CE. Choose attacks, heal, or swap monsters to defeat opponents.

Playable locally and in modern web browsers via WebAssembly ([Pygbag](https://pygame-web.github.io/)).

## How to Run Locally

### Prerequisites
- Python 3.10+
- `pip install pygame-ce pygbag`

### Play Locally
```bash
python main.py
```

### Run in Browser Locally
```bash
python -m pygbag main.py
```
Open `http://localhost:8000` in your web browser.

## Controls
- **Mouse Click**: Select attack, heal, or switch monster
- **Space**: Restart after game over
- **Escape**: Quit game
