"""
Thuật toán Minimax cho AI
Minimax algorithm for AI decision making
"""

import time
import math
from config import MAX_DEPTH, AI, HUMAN
from evaluation import evaluate, SCORE_WIN, SCORE_LOSE


# ═══════════════════════════════════════════════════════════════════
#                    THỐNG KÊ THUẬT TOÁN
# ═══════════════════════════════════════════════════════════════════

stats = {
    "states": 0,        # Số nút đã xét
    "depth": MAX_DEPTH, # Độ sâu tìm kiếm
    "value": 0,         # Giá trị của nước đi tốt nhất
    "time": 0.0,        # Thời gian tính toán
    "move": None        # Nước đi được chọn (r, c)
}


def minimax(board, depth, is_maximizing):
    """
    Thuật toán Minimax thuần túy (không có Alpha-Beta Pruning) - Level 1.
    
    Minimax là thuật toán quay lui để tìm nước đi tối ưu:
    - Maximizing player (AI): Tìm nước đi có điểm cao nhất
    - Minimizing player (Người chơi): Giả sử cố tìm nước đi có điểm thấp nhất cho AI
    
    Args:
        board: Đối tượng Board (trạng thái bàn cờ hiện tại)
        depth: Độ sâu tìm kiếm còn lại (từ MAX_DEPTH xuống 0)
        is_maximizing: True nếu đang tìm nước đi tối đa (AI), False nếu tối thiểu (Người chơi)
        
    Returns:
        int: Giá trị đánh giá tốt nhất có thể đạt được
    """
    # Tăng bộ đếm số nút đã xét
    stats["states"] += 1

    # ─────────────── Kiểm tra trạng thái kết thúc ───────────────

    # Kiểm tra AI có thắng không
    win_ai, _ = board.check_win(AI)
    if win_ai:
        # AI thắng - trả về điểm cao, ưu tiên thắng sớm (có thêm depth)
        return SCORE_WIN + depth

    # Kiểm tra Người chơi có thắng không
    win_hum, _ = board.check_win(HUMAN)
    if win_hum:
        # Người chơi thắng (AI thua) - trả về điểm âm, điểm càng âm nếu thua sau
        return SCORE_LOSE - depth

    # Kiểm tra bàn cờ đầy hay độ sâu hết
    if board.is_full() or depth == 0:
        # Sử dụng hàm đánh giá heuristic
        return evaluate(board)

    # ─────────────── Lấy nước đi ứng cử viên ───────────────

    candidates = board.get_candidates()
    if not candidates:
        return evaluate(board)

    # ─────────────── Đệ quy theo hướng của Minimax ───────────────

    if is_maximizing:
        # Maximizing player (AI): tìm nước đi có giá trị cao nhất
        best = -math.inf
        for r, c in candidates:
            # Thử nước đi (r, c)
            board.place(r, c, AI)
            # Gọi đệ quy với minimizing (người chơi đi tiếp)
            val = minimax(board, depth - 1, False)
            # Hoàn tác nước đi
            board.undo()
            # Cập nhật giá trị tốt nhất
            if val > best:
                best = val
        return best
    else:
        # Minimizing player (Người chơi): tìm nước đi có giá trị thấp nhất
        best = math.inf
        for r, c in candidates:
            # Thử nước đi (r, c)
            board.place(r, c, HUMAN)
            # Gọi đệ quy với maximizing (AI đi tiếp)
            val = minimax(board, depth - 1, True)
            # Hoàn tác nước đi
            board.undo()
            # Cập nhật giá trị tốt nhất (thấp nhất)
            if val < best:
                best = val
        return best


def ai_move(board):
    """
    Chọn nước đi tốt nhất cho AI bằng thuật toán Minimax.
    Thực hiện tìm kiếm từ sâu MAX_DEPTH và cập nhật thống kê.
    
    Quá trình:
    1. Lấy danh sách nước đi ứng cử viên
    2. Với mỗi ứng cử viên, tính giá trị minimax
    3. Chọn nước đi có giá trị cao nhất
    4. Cập nhật thống kê (thời gian, số nút, giá trị)
    
    Args:
        board: Đối tượng Board (bàn cờ hiện tại)
        
    Returns:
        tuple: Tọa độ nước đi tốt nhất (r, c)
    """
    # Ghi lại thời gian bắt đầu
    t0 = time.time()
    
    # Đặt lại thống kê
    stats["states"] = 0
    stats["depth"] = MAX_DEPTH

    # Lấy nước đi ứng cử viên
    candidates = board.get_candidates()
    
    # Khởi tạo giá trị tốt nhất và nước đi tốt nhất
    best_val = -math.inf
    best_move = candidates[0] if candidates else None

    # Duyệt qua từng nước đi ứng cử viên
    for r, c in candidates:
        # Thử nước đi (r, c)
        board.place(r, c, AI)
        # Tính giá trị minimax với độ sâu MAX_DEPTH - 1
        # (depth = MAX_DEPTH là cho nước đi hiện tại, -1 cho nước đi tiếp theo)
        val = minimax(board, MAX_DEPTH - 1, False)
        # Hoàn tác nước đi
        board.undo()
        
        # Nếu tốt hơn, cập nhật
        if val > best_val:
            best_val = val
            best_move = (r, c)

    # Cập nhật thống kê
    stats["value"] = best_val
    stats["time"] = time.time() - t0
    stats["move"] = best_move
    
    return best_move
