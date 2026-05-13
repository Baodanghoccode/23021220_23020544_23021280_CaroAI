"""
Giao diện trò chơi Pygame
Game UI and main game loop using Pygame
"""

import pygame
import sys
from config import (
    BOARD_SIZE, WIN_COUNT, MARGIN, CELL_SIZE, BOARD_PX, WIN_W, WIN_H, INFO_HEIGHT,
    C_BG, C_BOARD_BG, C_GRID, C_GRID_BOLD, C_X, C_O, C_WIN_LINE, C_TEXT, C_TEXT_DIM,
    C_PANEL, C_BTN, C_BTN_HOVER, C_BTN_TEXT, C_STATUS_WIN, C_STATUS_LOSE, C_STATUS_DRAW,
    C_HIGHLIGHT, EMPTY, HUMAN, AI, WINDOW_TITLE
)
from board import Board
from minimax import ai_move, stats


class Game:
    """
    Lớp quản lý trò chơi chính.
    
    Chức năng:
    - Khởi tạo cửa sổ Pygame
    - Vẽ bàn cờ và giao diện
    - Xử lý sự kiện (click chuột, bàn phím)
    - Quản lý vòng lặp trò chơi
    """

    def __init__(self):
        """Khởi tạo trò chơi."""
        # Tạo cửa sổ
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.clock = pygame.time.Clock()

        # Font cho text
        self.font_lg = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 16)
        self.font_sm = pygame.font.SysFont("consolas", 13)
        self.font_btn = pygame.font.SysFont("consolas", 15, bold=True)

        # Khởi tạo trò chơi
        self.reset()

    def reset(self):
        """
        Đặt lại trò chơi về trạng thái ban đầu.
        Dùng khi bắt đầu hoặc chơi lại.
        """
        self.board = Board()
        self.turn = HUMAN              # Người chơi đi trước
        self.game_over = False
        self.winner = None              # None = hòa
        self.win_cells = []             # Danh sách ô tạo đường thắng
        self.last_move = None           # Nước đi cuối cùng
        
        # Đặt lại thống kê
        stats["states"] = stats["value"] = stats["time"] = 0
        stats["move"] = None

    # ═════════════════════════════════════════════════════════════

    def draw_board(self):
        """Vẽ bàn cờ và các quân cờ."""
        # Vẽ hình chữ nhật nền bàn cờ
        board_rect = pygame.Rect(MARGIN, MARGIN, BOARD_PX, BOARD_PX)
        pygame.draw.rect(self.screen, C_BOARD_BG, board_rect, border_radius=4)

        # Vẽ lưới
        for i in range(BOARD_SIZE + 1):
            # Viền ngoài đậm hơn
            is_bold = (i == 0 or i == BOARD_SIZE)
            color = C_GRID_BOLD if is_bold else C_GRID
            width = 2 if is_bold else 1
            
            # Vẽ đường ngang
            y = MARGIN + i * CELL_SIZE
            pygame.draw.line(self.screen, color,
                             (MARGIN, y), (MARGIN + BOARD_PX, y), width)
            
            # Vẽ đường dọc
            x = MARGIN + i * CELL_SIZE
            pygame.draw.line(self.screen, color,
                             (x, MARGIN), (x, MARGIN + BOARD_PX), width)

        # Highlight ô vừa đánh (bán trong suốt)
        if self.last_move:
            lr, lc = self.last_move
            highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(C_HIGHLIGHT)
            self.screen.blit(highlight_surface, (MARGIN + lc * CELL_SIZE, MARGIN + lr * CELL_SIZE))

        # Vẽ các quân cờ trên bàn
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                player = self.board.grid[r][c]
                if player == EMPTY:
                    continue
                
                # Tính tọa độ pixel tâm ô
                cx, cy = self._px(r, c)
                radius = CELL_SIZE // 2 - 10
                
                if player == HUMAN:
                    # Vẽ X (hai đường chéo)
                    color = C_X
                    offset = radius
                    pygame.draw.line(self.screen, color,
                                     (cx - offset, cy - offset), (cx + offset, cy + offset), 3)
                    pygame.draw.line(self.screen, color,
                                     (cx + offset, cy - offset), (cx - offset, cy + offset), 3)
                else:
                    # Vẽ O (hình tròn)
                    pygame.draw.circle(self.screen, C_O, (cx, cy), radius, 3)

        # Vẽ đường thắng nếu có
        if self.win_cells and len(self.win_cells) >= 2:
            start_pos = self._px(*self.win_cells[0])
            end_pos = self._px(*self.win_cells[-1])
            pygame.draw.line(self.screen, C_WIN_LINE, start_pos, end_pos, 5)
            # Vẽ các điểm tròn tại các ô thắng
            for wr, wc in self.win_cells:
                pygame.draw.circle(self.screen, C_WIN_LINE, self._px(wr, wc), 6)

    def draw_info(self):
        """Vẽ panel thông tin dưới bàn cờ."""
        panel_y = MARGIN * 2 + BOARD_PX
        
        # Vẽ nền panel
        panel_rect = pygame.Rect(0, panel_y, WIN_W, INFO_HEIGHT)
        pygame.draw.rect(self.screen, C_PANEL, panel_rect)
        pygame.draw.line(self.screen, C_GRID_BOLD, (0, panel_y), (WIN_W, panel_y), 1)

        x0, y0 = 18, panel_y + 12

        # ────────────── Trạng thái trò chơi ──────────────
        if self.game_over:
            if self.winner == HUMAN:
                msg = "Bạn thắng!  X WIN"
                color = C_STATUS_WIN
            elif self.winner == AI:
                msg = "Máy thắng!  O WIN"
                color = C_STATUS_LOSE
            else:
                msg = "Hòa!  DRAW"
                color = C_STATUS_DRAW
        else:
            if self.turn == HUMAN:
                msg, color = "Lượt của bạn  [X]", C_X
            else:
                msg, color = "Máy đang suy nghĩ...  [O]", C_O

        surf = self.font_lg.render(msg, True, color)
        self.screen.blit(surf, (x0, y0))

        # ────────────── Thống kê nước đi máy ──────────────
        y0 += 32
        if stats["move"]:
            r, c = stats["move"]
            line1 = f"Nước đi: ({r},{c})   Giá trị: {stats['value']:+d}   Độ sâu: {stats['depth']}"
            line2 = f"Trạng thái đã xét: {stats['states']:,}   Thời gian: {stats['time']:.3f}s"
            self.screen.blit(self.font_md.render(line1, True, C_TEXT), (x0, y0))
            self.screen.blit(self.font_md.render(line2, True, C_TEXT_DIM), (x0, y0 + 20))

        # ────────────── Ghi chú ──────────────
        y0 += 50
        hint = "X = Người chơi   O = Máy (Pure Minimax)   4 quân liên tiếp = THẮNG"
        self.screen.blit(self.font_sm.render(hint, True, C_TEXT_DIM), (x0, y0))

        # ────────────── Nút chơi lại ──────────────
        btn_w, btn_h = 140, 34
        btn_x = WIN_W - btn_w - 20
        btn_y = panel_y + (INFO_HEIGHT - btn_h) // 2
        self.btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        
        # Kiểm tra hover
        mx, my = pygame.mouse.get_pos()
        btn_color = C_BTN_HOVER if self.btn_rect.collidepoint(mx, my) else C_BTN
        
        # Vẽ nút
        pygame.draw.rect(self.screen, btn_color, self.btn_rect, border_radius=6)
        pygame.draw.rect(self.screen, C_GRID_BOLD, self.btn_rect, 1, border_radius=6)
        
        # Vẽ text trên nút
        lbl = self.font_btn.render("Chơi lại [R]", True, C_BTN_TEXT)
        self.screen.blit(lbl, (btn_x + (btn_w - lbl.get_width()) // 2,
                                btn_y + (btn_h - lbl.get_height()) // 2))

    # ═════════════════════════════════════════════════════════════

    def _px(self, r, c):
        """
        Chuyển tọa độ lưới (row, col) → tọa độ pixel (x, y) tâm ô.
        
        Args:
            r, c: Hàng và cột trên lưới
            
        Returns:
            tuple: (x, y) tọa độ pixel
        """
        x = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
        y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def _cell_from_mouse(self, mx, my):
        """
        Chuyển tọa độ chuột → tọa độ lưới (row, col).
        
        Args:
            mx, my: Tọa độ chuột pixel
            
        Returns:
            tuple: (r, c) tọa độ lưới
        """
        c = (mx - MARGIN) // CELL_SIZE
        r = (my - MARGIN) // CELL_SIZE
        return r, c

    # ═════════════════════════════════════════════════════════════

    def run(self):
        """
        Vòng lặp chính của trò chơi.
        
        Luồng:
        1. Vẽ bàn cờ và giao diện
        2. Nếu đến lượt AI, tính toán nước đi
        3. Xử lý sự kiện (click chuột, bàn phím)
        4. Kiểm tra thắng/hòa
        5. Lặp lại
        """
        ai_thinking = False

        while True:
            # ────────────── Vẽ giao diện ──────────────
            self.screen.fill(C_BG)
            self.draw_board()
            self.draw_info()
            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS

            # ────────────── AI đánh (nếu tới lượt AI) ──────────────
            if not self.game_over and self.turn == AI and not ai_thinking:
                ai_thinking = True
                
                # Vẽ lại để thể hiện "đang suy nghĩ..."
                self.screen.fill(C_BG)
                self.draw_board()
                self.draw_info()
                pygame.display.flip()

                # Tính toán nước đi AI
                move = ai_move(self.board)
                if move:
                    r, c = move
                    self.board.place(r, c, AI)
                    self.last_move = (r, c)
                    
                    # Kiểm tra AI thắng không
                    won, cells = self.board.check_win(AI)
                    if won:
                        self.game_over = True
                        self.winner = AI
                        self.win_cells = cells
                    # Kiểm tra hòa không
                    elif self.board.is_full():
                        self.game_over = True
                        self.winner = None
                    else:
                        # Chuyển lượt cho người chơi
                        self.turn = HUMAN
                
                ai_thinking = False

            # ────────────── Xử lý sự kiện ──────────────
            for event in pygame.event.get():
                # Đóng cửa sổ
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Bàn phím
                if event.type == pygame.KEYDOWN:
                    # Nhấn R để chơi lại
                    if event.key == pygame.K_r:
                        self.reset()

                # Chuột click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    # Nhấn nút "Chơi lại"
                    if hasattr(self, "btn_rect") and self.btn_rect.collidepoint(mx, my):
                        self.reset()
                        continue

                    # Đánh quân (nếu là lượt người chơi)
                    if not self.game_over and self.turn == HUMAN:
                        r, c = self._cell_from_mouse(mx, my)
                        # Kiểm tra tọa độ hợp lệ và ô trống
                        if self.board.is_valid(r, c) and self.board.grid[r][c] == EMPTY:
                            self.board.place(r, c, HUMAN)
                            self.last_move = (r, c)
                            
                            # Kiểm tra người chơi thắng không
                            won, cells = self.board.check_win(HUMAN)
                            if won:
                                self.game_over = True
                                self.winner = HUMAN
                                self.win_cells = cells
                            # Kiểm tra hòa không
                            elif self.board.is_full():
                                self.game_over = True
                                self.winner = None
                            else:
                                # Chuyển lượt cho AI
                                self.turn = AI
