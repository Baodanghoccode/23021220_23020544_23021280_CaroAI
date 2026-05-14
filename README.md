# CaroAI in Python

This project is a Caro AI practice assignment for the Artificial Intelligence course. It implements a playable Caro game between a human player and the computer.

The current version covers **Level 2**: the AI can use either **depth-limited Minimax** or **Alpha-Beta pruning** with the same search depth and heuristic evaluation function.

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
|-- source_code/
|   |-- board.py        # Board representation, legal moves, win/draw checking
|   |-- config.py       # Game settings, colors, search depth
|   |-- evaluation.py   # Heuristic board evaluation
|   |-- game.py         # Pygame interface and main game loop
|   |-- main.py         # Program entry point
|   `-- minimax.py      # Minimax, Alpha-Beta, and move statistics
|-- requirements.txt    # Required Python packages
`-- README.md
```

## 3. Installation

Python 3.8 or newer is recommended.

```bash
python --version
pip install -r requirements.txt
```

Main dependency:

```text
pygame>=2.0.0
```

## 4. How to Run

From the repository root, run:

```bash
python source_code/main.py
```

After the game window opens:

- Click an empty cell to place your `X`.
- The computer automatically calculates and places its `O`.
- Press `R` or click the `Restart [R]` button to restart the game.
- Press `M` or click the `Mode` button to switch the AI mode between Minimax and Alpha-Beta.

## 5. Implemented Algorithms

The AI supports two adversarial search algorithms for a two-player zero-sum game:

- **Minimax**: explores possible human and computer moves up to a depth limit.
- **Alpha-Beta pruning**: uses the same Minimax logic but cuts branches when `beta <= alpha`.
- The computer is the MAX player and chooses the move with the highest evaluation value.
- The human is the MIN player and is assumed to choose moves that reduce the computer's advantage.
- If the state is win, loss, or draw, the algorithm returns a terminal value.
- If the search reaches the depth limit, the algorithm uses the heuristic evaluation function.
- Candidate moves are generated near existing pieces to reduce the search space.
- Candidate moves are ordered by distance to the board center before expansion.
- Both algorithms use the same search depth and evaluation function when compared.

Level 2 improvement notes:

- **Generate only nearby candidate moves**: instead of expanding every empty cell on the board, `Board.get_candidates()` only returns empty cells near existing pieces. This reduces the branching factor and makes both Minimax and Alpha-Beta faster.
- **Center-first move ordering**: `_ordered_candidates()` sorts candidate moves by distance to the board center before search expansion. This is especially useful for Alpha-Beta because better early moves can help prune more branches.

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
- The running time for the selected algorithm.
- A comparison row for Minimax and Alpha-Beta on the same board state.
- The number of Alpha-Beta pruning cuts.

These values support the assignment requirement for measuring and comparing search performance.

## 8. Current Scope

This version covers Level 2 requirements:

- 9x9 board.
- Alternating turns between human and computer.
- Invalid moves on occupied cells are rejected.
- Game ends when a player gets 4 consecutive pieces or the board is full.
- Depth-limited Minimax is implemented.
- Alpha-Beta pruning is implemented.
- The AI mode can be switched between Minimax and Alpha-Beta.
- Both algorithms are run on the same current board state for comparison.
- A heuristic evaluation function is implemented.
- The selected move, value, depth, explored states, and running time are recorded.

## 9. Possible Level 3 Extensions

- Prepare at least 5 test board states.
- Compare explored states and running time between Minimax and Alpha-Beta in a table.
- Test multiple search depths, such as depth 1, 2, and 3.
- Analyze whether Alpha-Beta chooses the same move as Minimax.
- Analyze how search depth affects move quality.
- Discuss strengths, limitations, and possible future improvements.

## 10. References
- Minimax algorithm: https://en.wikipedia.org/wiki/Minimax
- Alpha-Beta pruning algorithm: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
- Pygame documentation: https://www.pygame.org/docs/
- Gomoku rules: https://en.wikipedia.org/wiki/Gomoku
