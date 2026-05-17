# CaroAI in Python

This project is a Caro AI practice assignment for the Artificial Intelligence course. It implements a playable Caro game between a human player and the computer, then extends the implementation with Level 3 experimental benchmarking.

The current version covers **Level 3**:

- Level 1: depth-limited Minimax with a heuristic evaluation function.
- Level 2: Alpha-Beta pruning using the same depth and evaluation function as Minimax.
- Level 3: benchmark Minimax and Alpha-Beta on multiple board states and search depths, then export a result table and analysis report.

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
|   |-- level3.py       # Level 3 benchmark and report generator
|   |-- main.py         # Program entry point
|   `-- minimax.py      # Minimax, Alpha-Beta, and move statistics
|-- level3_results/
|   |-- benchmark_results.csv
|   `-- benchmark_report.md
|-- requirements.txt
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

## 4. How to Run the Game

From the repository root, run:

```bash
python source_code/main.py
```

After the game window opens:

- Click an empty cell to place your `X`.
- The computer automatically calculates and places its `O`.
- Press `R` or click the `Restart [R]` button to restart the game.
- Press `M` or click the `Mode` button to switch the AI mode between Minimax and Alpha-Beta.

## 5. How to Run Level 3 Benchmark

From the repository root, run:

```bash
python source_code/level3.py
```

The benchmark script:

- Creates 5 fixed test board states.
- Runs Minimax and Alpha-Beta on each state.
- Tests search depths `1`, `2`, and `3`.
- Uses the same move generator, search depth, and evaluation function for a fair comparison.
- Prints a comparison table to the console.
- Writes generated results to `level3_results/benchmark_results.csv`.
- Writes the analysis report to `level3_results/benchmark_report.md`.

## 6. Implemented Algorithms

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

Main configuration in `source_code/config.py`:

```python
BOARD_SIZE = 9
WIN_COUNT = 4
MAX_DEPTH = 3
```

## 7. Evaluation Function

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

## 8. Runtime Statistics

After each computer move, the interface displays:

- The selected move.
- The evaluation value.
- The search depth.
- The number of explored states.
- The running time for the selected algorithm.
- A comparison row for Minimax and Alpha-Beta on the same board state.
- The number of Alpha-Beta pruning cuts.

These values support the assignment requirement for measuring and comparing search performance.

## 9. Level 3 Experiment Design

The benchmark in `source_code/level3.py` includes these states:

1. **Opening**: empty board.
2. **Mid Game**: balanced middle-game state.
3. **AI Can Win**: AI has an immediate winning threat.
4. **Must Block**: human has an immediate three-in-a-row threat.
5. **Many Branches**: crowded non-terminal state with many legal candidate moves.

For each state, the benchmark records:

- Minimax move and Alpha-Beta move.
- Whether both algorithms choose the same move.
- Evaluation values.
- Explored states.
- Alpha-Beta prune count.
- Runtime.
- State reduction percentage.
- Runtime speedup.

## 10. References

- Minimax algorithm: https://en.wikipedia.org/wiki/Minimax
- Alpha-Beta pruning algorithm: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
- Pygame documentation: https://www.pygame.org/docs/
- Gomoku rules: https://en.wikipedia.org/wiki/Gomoku
- Reference repository: https://github.com/MonHauVD/Caro_AI
