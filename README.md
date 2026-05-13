# CaroAI in Python

This is a simple [Caro](https://vi.wikipedia.org/wiki/C%E1%BB%9D_ca-r%C3%B4) AI implemented in Python.

The current version focuses on **Level 1**: the AI uses **depth-limited Minimax** with a heuristic evaluation function to choose its moves.

## 1. Overview

- Game: Human vs AI Caro.
- Interface: Pygame.
- Board size: 9x9.
- Human player: `X`.
- AI player: `O`.
- Win condition: 4 consecutive pieces horizontally, vertically, or diagonally.
- The double-block rule is not considered.
- The game is a draw if the board is full and no player has won.

## 2. Project Structure

```text
23021220_23020544_23021280_CaroAI/
├── source_code/
│   ├── board.py        # Board representation, legal moves, win/draw checking
│   ├── config.py       # Game settings, colors, search depth
│   ├── evaluation.py   # Heuristic board evaluation
│   ├── game.py         # Pygame interface and main game loop
│   ├── main.py         # Program entry point
│   └── minimax.py      # Minimax algorithm and move statistics
├── requirements.txt    # Required Python packages
└── README.md
```

## 3. Installation

Python 3.8 or newer is recommended.

```bash
python --version
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Main dependency:

```text
pygame>=2.0.0
```

## 4. How to Run the game

From the repository root, run:

```bash
python source_code/main.py
```

After the game window opens:

- Click an empty cell to place your `X`.
- The computer automatically calculates and places its `O`.
- Press `R` or click the `Choi lai [R]` button to restart the game.

## 5. Implemented Algorithm

The AI uses Minimax for a two-player zero-sum game:

- The computer is the MAX player and chooses the move with the highest evaluation value.
- The human is the MIN player and is assumed to choose moves that reduce the computer's advantage.
- If the state is win, loss, or draw, the algorithm returns a terminal value.
- If the search reaches the depth limit, the algorithm uses the heuristic evaluation function.
- Candidate moves are generated near existing pieces to reduce the search space.

Main configuration in `source_code/config.py`:

```python
BOARD_SIZE = 9
WIN_COUNT = 4
MAX_DEPTH = 3
```

## 6. Evaluation Function

The evaluation function in `source_code/evaluation.py` scores piece sequences in 4 directions: horizontal, vertical, and the 2 diagonals.

Main scoring rules:

| Situation | Score |
| --- | ---: |
| Computer has 4 consecutive pieces | +100000 |
| Human has 4 consecutive pieces | -100000 |
| Computer has 3 pieces with 2 open ends | +5000 |
| Computer has 3 pieces with 1 open end | +500 |
| Computer has 2 pieces with 2 open ends | +100 |
| Similar human sequences | Negative score, multiplied by 2 to prioritize blocking |

## 7. Runtime Statistics

After each computer move, the interface displays:

- The selected move.
- The evaluation value.
- The search depth.
- The number of explored states.
- The running time for the move calculation.

These values support the assignment requirement for measuring and analyzing search performance.

## 8. Current Scope

This version covers Level 1 requirements:

- 9x9 board.
- Alternating turns between human and computer.
- Invalid moves on occupied cells are rejected.
- Game ends when a player gets 4 consecutive pieces or the board is full.
- Depth-limited Minimax is implemented.
- A heuristic evaluation function is implemented.
- The selected move, value, depth, explored states, and running time are recorded.

## 9. Possible extensions:

- Implement Alpha-Beta pruning.
- Allow choosing between Minimax and Alpha-Beta AI modes.
- Prepare at least 5 test board states.
- Compare explored states and running time between Minimax and Alpha-Beta.
- Create an experiment table and analyze the effect of search depth.

## 10. References
- Minimax algorithm: https://en.wikipedia.org/wiki/Minimax
- Pygame documentation: https://www.pygame.org/docs/
- Gomoku rules: https://en.wikipedia.org/wiki/Gomoku
