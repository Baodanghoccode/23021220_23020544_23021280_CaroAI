"""
Level 3 benchmark: compare Minimax and Alpha-Beta on fixed Caro states.

Run from the repository root:
    python source_code/level3.py

The script writes:
    level3_results/benchmark_results.csv
    level3_results/benchmark_report.md
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from board import Board
from config import AI, EMPTY, HUMAN
from minimax_with_alphabeta import ALPHA_BETA, MINIMAX, choose_move


DEPTHS = (1, 2, 3)
RESULT_DIR = Path(__file__).resolve().parents[1] / "level3_results"
CSV_PATH = RESULT_DIR / "benchmark_results.csv"
REPORT_PATH = RESULT_DIR / "benchmark_report.md"


@dataclass
class TestBoard:
    name: str
    description: str
    board: Board


def place_many(board: Board, moves: list[tuple[int, int, int]]) -> Board:
    for row, col, player in moves:
        board.place(row, col, player)
    return board


def setup_test_boards() -> list[TestBoard]:
    """Create the required five board states for Level 3 experiments."""
    boards: list[TestBoard] = []

    boards.append(
        TestBoard(
            "Opening",
            "Empty board. This verifies the first move and baseline branching.",
            Board(),
        )
    )

    boards.append(
        TestBoard(
            "Mid Game",
            "A balanced middle-game state with both attack and defense options.",
            place_many(
                Board(),
                [
                    (4, 4, AI),
                    (3, 3, HUMAN),
                    (4, 5, AI),
                    (5, 4, HUMAN),
                    (3, 5, AI),
                    (5, 5, HUMAN),
                ],
            ),
        )
    )

    boards.append(
        TestBoard(
            "AI Can Win",
            "AI already has three connected pieces and should finish the row.",
            place_many(
                Board(),
                [
                    (4, 4, AI),
                    (4, 5, AI),
                    (4, 6, AI),
                    (3, 3, HUMAN),
                    (5, 3, HUMAN),
                ],
            ),
        )
    )

    boards.append(
        TestBoard(
            "Must Block",
            "The human has an immediate three-in-a-row threat, so AI should block.",
            place_many(
                Board(),
                [
                    (4, 4, HUMAN),
                    (4, 5, HUMAN),
                    (4, 6, HUMAN),
                    (4, 7, AI),
                    (3, 3, AI),
                ],
            ),
        )
    )

    boards.append(
        TestBoard(
            "Many Branches",
            "A non-terminal crowded center that creates many legal candidate moves.",
            place_many(
                Board(),
                [
                    (4, 4, AI),
                    (3, 4, AI),
                    (5, 3, AI),
                    (3, 6, AI),
                    (6, 5, AI),
                    (4, 5, HUMAN),
                    (5, 4, HUMAN),
                    (3, 3, HUMAN),
                    (5, 6, HUMAN),
                    (2, 5, HUMAN),
                ],
            ),
        )
    )

    return boards


def board_to_text(board: Board) -> str:
    symbols = {EMPTY: ".", HUMAN: "X", AI: "O"}
    return "\n".join(" ".join(symbols[cell] for cell in row) for row in board.grid)


def pct_reduction(minimax_states: int, alpha_beta_states: int) -> float:
    if minimax_states <= 0:
        return 0.0
    return max(0.0, 100.0 * (1.0 - alpha_beta_states / minimax_states))


def speedup(minimax_time: float, alpha_beta_time: float) -> float:
    if alpha_beta_time <= 0:
        return 0.0
    return minimax_time / alpha_beta_time


def run_benchmark() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    for test_board in setup_test_boards():
        for depth in DEPTHS:
            minimax_result = choose_move(test_board.board.copy(), MINIMAX, depth)
            alpha_beta_result = choose_move(test_board.board.copy(), ALPHA_BETA, depth)

            mm_states = int(minimax_result["states"])
            ab_states = int(alpha_beta_result["states"])
            mm_time = float(minimax_result["time"])
            ab_time = float(alpha_beta_result["time"])

            results.append(
                {
                    "board": test_board.name,
                    "description": test_board.description,
                    "depth": depth,
                    "minimax_move": minimax_result["move"],
                    "alpha_beta_move": alpha_beta_result["move"],
                    "same_move": minimax_result["move"] == alpha_beta_result["move"],
                    "minimax_value": minimax_result["value"],
                    "alpha_beta_value": alpha_beta_result["value"],
                    "minimax_states": mm_states,
                    "alpha_beta_states": ab_states,
                    "state_reduction_pct": pct_reduction(mm_states, ab_states),
                    "alpha_beta_prunes": alpha_beta_result["prunes"],
                    "minimax_time_sec": mm_time,
                    "alpha_beta_time_sec": ab_time,
                    "speedup": speedup(mm_time, ab_time),
                }
            )

    return results


def write_csv(results: list[dict[str, object]]) -> None:
    RESULT_DIR.mkdir(exist_ok=True)
    fields = [
        "board",
        "depth",
        "minimax_move",
        "alpha_beta_move",
        "same_move",
        "minimax_value",
        "alpha_beta_value",
        "minimax_states",
        "alpha_beta_states",
        "state_reduction_pct",
        "alpha_beta_prunes",
        "minimax_time_sec",
        "alpha_beta_time_sec",
        "speedup",
    ]

    with CSV_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in results:
            writer.writerow({field: row[field] for field in fields})


def rows_for_depth(results: list[dict[str, object]], depth: int) -> list[dict[str, object]]:
    return [row for row in results if row["depth"] == depth]


def avg(rows: list[dict[str, object]], key: str) -> float:
    return mean(float(row[key]) for row in rows) if rows else 0.0


def markdown_table(results: list[dict[str, object]]) -> str:
    lines = [
        "| Board | D | Minimax Move | Alpha-Beta Move | Same | MM States | AB States | Reduction | AB Prunes | MM Time | AB Time | Speedup |",
        "| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in results:
        same = "yes" if row["same_move"] else "no"
        lines.append(
            "| {board} | {depth} | {mm_move} | {ab_move} | {same} | {mm_states:,} | "
            "{ab_states:,} | {reduction:.1f}% | {prunes:,} | {mm_time:.4f}s | "
            "{ab_time:.4f}s | {speedup:.2f}x |".format(
                board=row["board"],
                depth=row["depth"],
                mm_move=row["minimax_move"],
                ab_move=row["alpha_beta_move"],
                same=same,
                mm_states=row["minimax_states"],
                ab_states=row["alpha_beta_states"],
                reduction=row["state_reduction_pct"],
                prunes=row["alpha_beta_prunes"],
                mm_time=row["minimax_time_sec"],
                ab_time=row["alpha_beta_time_sec"],
                speedup=row["speedup"],
            )
        )

    return "\n".join(lines)


def write_report(results: list[dict[str, object]]) -> None:
    RESULT_DIR.mkdir(exist_ok=True)
    boards = setup_test_boards()
    same_count = sum(1 for row in results if row["same_move"])
    total = len(results)
    overall_reduction = pct_reduction(
        sum(int(row["minimax_states"]) for row in results),
        sum(int(row["alpha_beta_states"]) for row in results),
    )
    avg_speedup = avg(results, "speedup")

    depth_lines = []
    for depth in DEPTHS:
        rows = rows_for_depth(results, depth)
        depth_lines.append(
            "- Depth {depth}: average state reduction {reduction:.1f}%, "
            "average speedup {speedup:.2f}x, average Minimax time {mm_time:.4f}s, "
            "average Alpha-Beta time {ab_time:.4f}s.".format(
                depth=depth,
                reduction=avg(rows, "state_reduction_pct"),
                speedup=avg(rows, "speedup"),
                mm_time=avg(rows, "minimax_time_sec"),
                ab_time=avg(rows, "alpha_beta_time_sec"),
            )
        )

    board_sections = []
    for test_board in boards:
        board_sections.append(
            "### {name}\n{description}\n\n```text\n{board}\n```".format(
                name=test_board.name,
                description=test_board.description,
                board=board_to_text(test_board.board),
            )
        )

    report = f"""# Level 3 Experimental Report

## 1. Goal
This report evaluates the implemented Minimax and Alpha-Beta pruning algorithms on five fixed Caro board states. Both algorithms use the same move generator, the same heuristic evaluation function, and the same search depths for each comparison.

## 2. Test Board States
{chr(10).join(board_sections)}

## 3. Result Table
{markdown_table(results)}

## 4. Analysis
- Alpha-Beta selected the same move as Minimax in {same_count}/{total} experiments ({same_count / total * 100:.1f}%).
- Across all experiments, Alpha-Beta reduced explored states by {overall_reduction:.1f}% compared with Minimax.
- The average runtime speedup was {avg_speedup:.2f}x. Small depths can show little speedup because there are few branches to prune.
{chr(10).join(depth_lines)}

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
"""

    REPORT_PATH.write_text(report, encoding="utf-8")


def print_summary(results: list[dict[str, object]]) -> None:
    print("=" * 120)
    print("LEVEL 3: MINIMAX VS ALPHA-BETA BENCHMARK")
    print("=" * 120)
    print(
        f"{'Board':<14} {'D':<2} {'MM Move':<10} {'AB Move':<10} {'Same':<5} "
        f"{'MM States':>10} {'AB States':>10} {'Reduce':>9} {'Prunes':>8} {'Speedup':>8}"
    )
    print("-" * 120)

    for row in results:
        print(
            f"{row['board']:<14} {row['depth']:<2} {str(row['minimax_move']):<10} "
            f"{str(row['alpha_beta_move']):<10} {str(row['same_move']):<5} "
            f"{row['minimax_states']:>10,} {row['alpha_beta_states']:>10,} "
            f"{row['state_reduction_pct']:>8.1f}% {row['alpha_beta_prunes']:>8,} "
            f"{row['speedup']:>7.2f}x"
        )

    print("-" * 120)
    print(f"Wrote CSV report: {CSV_PATH}")
    print(f"Wrote Markdown report: {REPORT_PATH}")


def main() -> None:
    results = run_benchmark()
    write_csv(results)
    write_report(results)
    print_summary(results)


if __name__ == "__main__":
    main()
