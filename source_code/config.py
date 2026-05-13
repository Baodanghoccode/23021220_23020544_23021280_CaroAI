"""
Cấu hình và hằng số cho trò chơi Cờ Caro
Configuration and constants for Caro game
"""

import pygame

# ═══════════════════════════════════════════════════════════════════
#                      THAM SỐ TRÒ CHƠI
# ═══════════════════════════════════════════════════════════════════

BOARD_SIZE = 9          # Kích thước bàn cờ (9x9)
WIN_COUNT = 4           # Số quân liên tiếp để thắng (4 quân)
MAX_DEPTH = 3           # Độ sâu tìm kiếm của Minimax (3 nước)

# ─────────────────────────── GIAO DIỆN ───────────────────────────

MARGIN = 30             # Lề bàn cờ (khoảng cách từ cạnh cửa sổ)
INFO_HEIGHT = 150       # Chiều cao panel thông tin dưới bàn cờ

# Tự động tính CELL_SIZE theo kích thước màn hình
# Auto-calculate CELL_SIZE based on screen resolution
pygame.init()
_info = pygame.display.Info()
_avail_w = int(_info.current_w * 0.90) - MARGIN * 2
_avail_h = int(_info.current_h * 0.90) - MARGIN * 2 - INFO_HEIGHT
CELL_SIZE = max(36, min(64, min(_avail_w, _avail_h) // BOARD_SIZE))

# Tính kích thước cửa sổ dựa trên kích thước bàn cờ
# Calculate window size based on board size
BOARD_PX = BOARD_SIZE * CELL_SIZE
WIN_W = BOARD_PX + MARGIN * 2
WIN_H = BOARD_PX + MARGIN * 2 + INFO_HEIGHT

# ═══════════════════════════════════════════════════════════════════
#                         BẢNG MÀU SẮC
# ═══════════════════════════════════════════════════════════════════

# Màu nền chính
C_BG = (15, 20, 35)
C_BOARD_BG = (22, 30, 50)

# Màu lưới
C_GRID = (45, 60, 90)           # Lưới bình thường
C_GRID_BOLD = (70, 90, 130)     # Lưới đậm (viền ngoài)

# Màu quân
C_X = (80, 200, 255)            # Quân người chơi (X) - xanh lam
C_O = (255, 100, 100)           # Quân máy (O) - đỏ

# Màu trạng thái
C_WIN_LINE = (255, 220, 50)     # Đường thắng - vàng
C_HIGHLIGHT = (255, 220, 50, 60)  # Highlight nước đi cuối cùng (có độ trong suốt)

# Màu text
C_TEXT = (200, 210, 230)        # Text chính
C_TEXT_DIM = (100, 115, 140)    # Text mờ

# Màu panel thông tin
C_PANEL = (18, 25, 42)          # Nền panel
C_BTN = (40, 55, 85)            # Nút bình thường
C_BTN_HOVER = (60, 80, 120)     # Nút khi hover
C_BTN_TEXT = (180, 195, 220)    # Text trên nút

# Màu trạng thái trò chơi
C_STATUS_WIN = (80, 220, 130)   # Thắng - xanh lá
C_STATUS_LOSE = (255, 100, 100) # Thua - đỏ
C_STATUS_DRAW = (200, 180, 80)  # Hòa - cam

# ═══════════════════════════════════════════════════════════════════
#                      HẰNG SỐ TRẠNG THÁI
# ═══════════════════════════════════════════════════════════════════

# Ký hiệu trên bàn cờ
EMPTY = 0               # Ô trống
HUMAN = 1               # Người chơi (X)
AI = 2                  # Máy tính (O)

# ─────────────────────────── TIÊU ĐỀ CỬA SỔ ───────────────────────

WINDOW_TITLE = "Cờ Caro – Pure Minimax AI (Level 1)"
