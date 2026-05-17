# Level 3 Experimental Report

## 1. Goal
This report evaluates the implemented Minimax and Alpha-Beta pruning algorithms on five fixed Caro board states. Both algorithms use the same move generator, the same heuristic evaluation function, and the same search depths for each comparison.

## 2. Test Board States
### Opening
Empty board. This verifies the first move and baseline branching.

```text
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
### Mid Game
A balanced middle-game state with both attack and defense options.

```text
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . X . O . . .
. . . . O O . . .
. . . . X X . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
### AI Can Win
AI already has three connected pieces and should finish the row.

```text
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . X . . . . .
. . . . O O O . .
. . . X . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
### Must Block
The human has an immediate three-in-a-row threat, so AI should block.

```text
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . O . . . . .
. . . . X X X O .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
```
### Many Branches
A non-terminal crowded center that creates many legal candidate moves.

```text
. . . . . . . . .
. . . . . . . . .
. . . . . X . . .
. . . X O . O . .
. . . . O X . . .
. . . O X . X . .
. . . . . O . . .
. . . . . . . . .
. . . . . . . . .
```

## 3. Result Table
| Board | D | Minimax Move | Alpha-Beta Move | Same | MM States | AB States | Reduction | AB Prunes | MM Time | AB Time | Speedup |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Opening | 1 | (4, 4) | (4, 4) | yes | 1 | 1 | 0.0% | 0 | 0.0000s | 0.0000s | 1.47x |
| Opening | 2 | (4, 4) | (4, 4) | yes | 25 | 25 | 0.0% | 0 | 0.0007s | 0.0007s | 1.01x |
| Opening | 3 | (4, 4) | (4, 4) | yes | 841 | 78 | 90.7% | 23 | 0.0281s | 0.0024s | 11.68x |
| Mid Game | 1 | (5, 3) | (5, 3) | yes | 41 | 41 | 0.0% | 0 | 0.0020s | 0.0022s | 0.94x |
| Mid Game | 2 | (5, 3) | (5, 3) | yes | 1,931 | 1,931 | 0.0% | 0 | 0.1080s | 0.1088s | 0.99x |
| Mid Game | 3 | (4, 3) | (4, 3) | yes | 95,998 | 12,153 | 87.3% | 1,774 | 6.2177s | 0.8280s | 7.51x |
| AI Can Win | 1 | (4, 3) | (4, 3) | yes | 45 | 45 | 0.0% | 0 | 0.0021s | 0.0021s | 1.00x |
| AI Can Win | 2 | (4, 3) | (4, 3) | yes | 2,169 | 2,169 | 0.0% | 0 | 0.1232s | 0.1198s | 1.03x |
| AI Can Win | 3 | (4, 3) | (4, 3) | yes | 113,637 | 8,891 | 92.2% | 2,081 | 6.6784s | 0.4610s | 14.49x |
| Must Block | 1 | (4, 3) | (4, 3) | yes | 39 | 39 | 0.0% | 0 | 0.0018s | 0.0024s | 0.74x |
| Must Block | 2 | (4, 3) | (4, 3) | yes | 1,761 | 1,761 | 0.0% | 0 | 0.0982s | 0.0959s | 1.02x |
| Must Block | 3 | (4, 3) | (4, 3) | yes | 82,895 | 5,375 | 93.5% | 1,643 | 5.1465s | 0.3493s | 14.73x |
| Many Branches | 1 | (3, 5) | (3, 5) | yes | 56 | 56 | 0.0% | 0 | 0.0038s | 0.0040s | 0.94x |
| Many Branches | 2 | (3, 5) | (3, 5) | yes | 3,252 | 3,252 | 0.0% | 0 | 0.2637s | 0.2603s | 1.01x |
| Many Branches | 3 | (3, 5) | (3, 5) | yes | 188,430 | 17,144 | 90.9% | 3,038 | 16.4162s | 1.6008s | 10.25x |

## 4. Analysis
- Alpha-Beta selected the same move as Minimax in 15/15 experiments (100.0%).
- Across all experiments, Alpha-Beta reduced explored states by 89.2% compared with Minimax.
- The average runtime speedup was 4.59x. Small depths can show little speedup because there are few branches to prune.
- Depth 1: average state reduction 0.0%, average speedup 1.02x, average Minimax time 0.0020s, average Alpha-Beta time 0.0022s.
- Depth 2: average state reduction 0.0%, average speedup 1.01x, average Minimax time 0.1188s, average Alpha-Beta time 0.1171s.
- Depth 3: average state reduction 90.9%, average speedup 11.73x, average Minimax time 6.8974s, average Alpha-Beta time 0.6483s.

## 5. Depth Impact
Depth 1 reacts mostly to immediate heuristic scores, so it is useful for quick tactical checks but can miss replies from the human player. Depth 2 includes the human response and can choose safer defensive moves. Depth 3 usually gives better tactical quality because it can see one more AI move after the human response, but it greatly increases the number of states for plain Minimax.

## 6. Evaluation Function
Strengths:
- It detects terminal wins and losses with very large scores.
- It gives high value to open three-in-a-row patterns.
- Human threats are weighted negatively, so blocking is prioritized.

Limitations:
- It does not fully understand advanced forcing patterns or long-term positional plans.
- The coefficients are manually chosen and may not be optimal for every board state.
- It evaluates visible line patterns, so deeper search is still needed for stronger play.

## 7. AI Behavior
The AI performs well on immediate winning and blocking positions because these patterns are directly represented in the heuristic and terminal checks. It is weaker in crowded positions where several moves have similar heuristic scores, because the evaluation function has limited strategic knowledge.

## 8. Future Improvements
- Improve move ordering by scoring candidate threats before search expansion.
- Add a transposition table to reuse repeated board evaluations.
- Add a per-move time budget and iterative deepening for larger boards or higher search depths.
