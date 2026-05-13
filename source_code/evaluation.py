"""
Hàm đánh giá trạng thái bàn cờ (Heuristic Evaluation)
Evaluation functions for board state assessment
"""

from config import EMPTY, HUMAN, AI, WIN_COUNT


# ═══════════════════════════════════════════════════════════════════
#                      HỆ SỐ ĐIỂM TẢI
# ═══════════════════════════════════════════════════════════════════

SCORE_WIN = 100_000         # Điểm khi AI thắng
SCORE_LOSE = -100_000       # Điểm khi AI thua (người chơi thắng)
SCORE_DRAW = 0              # Điểm khi hòa


def score_line(count, open_ends, is_ai):
    """
    Tính điểm cho một đoạn quân liên tiếp dựa vào số quân và số đầu mở.
    
    Ví dụ:
    - 4 quân liên tiếp = thắng (100,000 điểm)
    - 3 quân + 2 đầu mở = nguy hiểm (5,000 điểm)
    - 2 quân + 2 đầu mở = tiềm năng (100 điểm)
    
    Args:
        count: Số quân liên tiếp (ví dụ 1, 2, 3, hoặc 4)
        open_ends: Số đầu mở (0, 1, hoặc 2)
        is_ai: True nếu là quân của AI, False nếu là quân của người chơi
        
    Returns:
        int: Điểm số (dương cho AI, âm cho người chơi)
    """
    # Điểm cơ bản
    base = 0
    if count >= WIN_COUNT:
        base = SCORE_WIN
    elif count == 3 and open_ends == 2:
        base = 5_000        # 3 quân với 2 đầu mở - rất nguy hiểm
    elif count == 3 and open_ends == 1:
        base = 500          # 3 quân với 1 đầu mở - nguy hiểm vừa
    elif count == 2 and open_ends == 2:
        base = 100          # 2 quân với 2 đầu mở - có tiềm năng
    elif count == 2 and open_ends == 1:
        base = 10           # 2 quân với 1 đầu mở - tiềm năng nhỏ
    else:
        base = 1            # 1 quân hoặc không có đầu mở - không quan trọng
    
    # Nếu là quân AI, giữ nguyên điểm; nếu là quân người chơi, âm hóa x2
    # (chặn người chơi được ưu tiên cao hơn)
    if is_ai:
        return base
    else:
        return -base * 2    # Chặn được ưu tiên cao hơn bắt được


def evaluate(board) -> int:
    """
    Hàm đánh giá heuristic cho trạng thái bàn cờ chưa kết thúc.
    Cộng điểm của tất cả các đoạn quân trên bàn.
    
    Args:
        board: Đối tượng Board
        
    Returns:
        int: Tổng điểm (dương: lợi cho AI, âm: lợi cho người chơi)
    """
    total = 0
    # 4 hướng kiểm tra: ngang, dọc, chéo /, chéo \\
    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]

    # Kiểm tra từng người chơi
    for player in (AI, HUMAN):
        is_ai = (player == AI)
        
        # Duyệt từng ô
        for r in range(board.size):
            for c in range(board.size):
                # Bỏ qua ô không phải của player
                if board.grid[r][c] != player:
                    continue
                
                # Kiểm tra 4 hướng từ ô này
                for dr, dc in dirs:
                    # Kiểm tra nếu ô trước đó cũng là của player (tránh đếm 2 lần)
                    pr, pc = r - dr, c - dc
                    if board.is_valid(pr, pc) and board.grid[pr][pc] == player:
                        continue    # Đã tính từ ô trước
                    
                    # Đếm quân liên tiếp theo hướng này
                    count = 1
                    nr, nc = r + dr, c + dc
                    while board.is_valid(nr, nc) and board.grid[nr][nc] == player:
                        count += 1
                        nr += dr
                        nc += dc
                    
                    # Kiểm tra số đầu mở (ô trống ở hai đầu)
                    open_ends = 0
                    # Kiểm tra đầu trước
                    if board.is_valid(r - dr, c - dc) and board.grid[r - dr][c - dc] == EMPTY:
                        open_ends += 1
                    # Kiểm tra đầu sau
                    if board.is_valid(nr, nc) and board.grid[nr][nc] == EMPTY:
                        open_ends += 1
                    
                    # Cộng điểm
                    total += score_line(count, open_ends, is_ai)
    
    return total
