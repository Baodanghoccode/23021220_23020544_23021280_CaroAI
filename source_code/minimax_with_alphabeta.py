"""
Minimax and Alpha-Beta search for the Caro AI.
"""

import math
import time

from config import AI, HUMAN, MAX_DEPTH
from evaluation import SCORE_DRAW, SCORE_LOSE, SCORE_WIN, evaluate


MINIMAX = "minimax"
ALPHA_BETA = "alpha_beta"
AI_MODES = (MINIMAX, ALPHA_BETA)

stats = {
    "mode": ALPHA_BETA,
    "states": 0,
    "depth": MAX_DEPTH,
    "value": 0,
    "time": 0.0,
    "move": None,
    "comparison": {},
}


def _terminal_value(board, depth):
    """Return a terminal score, or None when the game should continue."""
    win_ai, _ = board.check_win(AI)
    if win_ai:
        return SCORE_WIN + depth

    win_human, _ = board.check_win(HUMAN)
    if win_human:
        return SCORE_LOSE - depth

    if board.is_full():
        return SCORE_DRAW

    return None


def _ordered_candidates(board):
    """Return legal candidate moves in a stable center-first order."""
    center = board.size // 2
    return sorted(
        board.get_candidates(),
        key=lambda move: (abs(move[0] - center) + abs(move[1] - center), move[0], move[1]),
    )


def minimax(board, depth, is_maximizing, counter):
    """Pure depth-limited Minimax."""
    counter["states"] += 1

    terminal = _terminal_value(board, depth)
    if terminal is not None:
        return terminal

    if depth == 0:
        return evaluate(board)

    candidates = _ordered_candidates(board)
    if not candidates:
        return evaluate(board)

    if is_maximizing:
        best = -math.inf
        for r, c in candidates:
            board.place(r, c, AI)
            best = max(best, minimax(board, depth - 1, False, counter))
            board.undo()
        return best

    best = math.inf
    for r, c in candidates:
        board.place(r, c, HUMAN)
        best = min(best, minimax(board, depth - 1, True, counter))
        board.undo()
    return best


def alpha_beta(board, depth, is_maximizing, alpha, beta, counter):
    """Depth-limited Minimax with Alpha-Beta pruning."""
    counter["states"] += 1

    terminal = _terminal_value(board, depth)
    if terminal is not None:
        return terminal

    if depth == 0:
        return evaluate(board)

    candidates = _ordered_candidates(board)
    if not candidates:
        return evaluate(board)

    if is_maximizing:
        best = -math.inf
        for r, c in candidates:
            board.place(r, c, AI)
            best = max(best, alpha_beta(board, depth - 1, False, alpha, beta, counter))
            board.undo()

            alpha = max(alpha, best)
            if beta <= alpha:
                counter["prunes"] += 1
                break
        return best

    best = math.inf
    for r, c in candidates:
        board.place(r, c, HUMAN)
        best = min(best, alpha_beta(board, depth - 1, True, alpha, beta, counter))
        board.undo()

        beta = min(beta, best)
        if beta <= alpha:
            counter["prunes"] += 1
            break
    return best


def _score_candidate(board, mode, depth, counter):
    if mode == MINIMAX:
        return minimax(board, depth, False, counter)
    if mode == ALPHA_BETA:
        return alpha_beta(board, depth, False, -math.inf, math.inf, counter)
    raise ValueError(f"Unsupported AI mode: {mode}")


def choose_move(board, mode=ALPHA_BETA, depth=MAX_DEPTH):
    """
    Choose the best AI move using the requested algorithm.

    Returns a dictionary containing the chosen move, evaluation value, explored
    states, running time, search depth, and Alpha-Beta prune count.
    """
    if mode not in AI_MODES:
        raise ValueError(f"Unsupported AI mode: {mode}")
    if depth < 1:
        raise ValueError("Search depth must be at least 1")

    t0 = time.time()
    counter = {"states": 0, "prunes": 0}
    candidates = _ordered_candidates(board)

    best_move = candidates[0] if candidates else None
    best_value = -math.inf

    for r, c in candidates:
        board.place(r, c, AI)
        value = _score_candidate(board, mode, depth - 1, counter)
        board.undo()

        if value > best_value:
            best_value = value
            best_move = (r, c)

    if best_move is None:
        best_value = SCORE_DRAW

    return {
        "mode": mode,
        "move": best_move,
        "value": int(best_value),
        "depth": depth,
        "states": counter["states"],
        "prunes": counter["prunes"],
        "time": time.time() - t0,
    }


def compare_algorithms(board, depth=MAX_DEPTH):
    """Run Minimax and Alpha-Beta on the same board state."""
    return {
        MINIMAX: choose_move(board.copy(), MINIMAX, depth),
        ALPHA_BETA: choose_move(board.copy(), ALPHA_BETA, depth),
    }


def ai_move(board, mode=ALPHA_BETA):
    """
    Choose the AI move and record Level 2 comparison statistics.

    Both algorithms are run on the same current board with the same search depth
    and evaluation function. The returned move is taken from the selected mode.
    """
    comparison = compare_algorithms(board)
    selected = comparison[mode]

    stats["mode"] = mode
    stats["states"] = selected["states"]
    stats["depth"] = selected["depth"]
    stats["value"] = selected["value"]
    stats["time"] = selected["time"]
    stats["move"] = selected["move"]
    stats["comparison"] = comparison

    return selected["move"]
