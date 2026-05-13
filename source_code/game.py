"""
Pygame interface and main loop for the Caro AI game.
"""

import sys

import pygame

from board import Board
from config import (
    AI,
    BOARD_PX,
    BOARD_SIZE,
    C_BG,
    C_BOARD_BG,
    C_BTN,
    C_BTN_HOVER,
    C_BTN_TEXT,
    C_GRID,
    C_GRID_BOLD,
    C_HIGHLIGHT,
    C_O,
    C_PANEL,
    C_STATUS_DRAW,
    C_STATUS_LOSE,
    C_STATUS_WIN,
    C_TEXT,
    C_TEXT_DIM,
    C_WIN_LINE,
    C_X,
    CELL_SIZE,
    EMPTY,
    HUMAN,
    INFO_HEIGHT,
    MARGIN,
    WIN_COUNT,
    WIN_H,
    WIN_W,
    WINDOW_TITLE,
)
from minimax import AI_MODES, ALPHA_BETA, ai_move, stats


class Game:
    """Main game controller."""

    def __init__(self):
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.clock = pygame.time.Clock()

        self.font_lg = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_md = pygame.font.SysFont("consolas", 16)
        self.font_sm = pygame.font.SysFont("consolas", 13)
        self.font_btn = pygame.font.SysFont("consolas", 15, bold=True)

        self.ai_mode = ALPHA_BETA
        self.reset()

    def reset(self):
        self.board = Board()
        self.turn = HUMAN
        self.game_over = False
        self.winner = None
        self.win_cells = []
        self.last_move = None

        stats["states"] = 0
        stats["value"] = 0
        stats["time"] = 0.0
        stats["move"] = None
        stats["comparison"] = {}

    def draw_board(self):
        board_rect = pygame.Rect(MARGIN, MARGIN, BOARD_PX, BOARD_PX)
        pygame.draw.rect(self.screen, C_BOARD_BG, board_rect, border_radius=4)

        for i in range(BOARD_SIZE + 1):
            is_border = i == 0 or i == BOARD_SIZE
            color = C_GRID_BOLD if is_border else C_GRID
            width = 2 if is_border else 1

            y = MARGIN + i * CELL_SIZE
            pygame.draw.line(self.screen, color, (MARGIN, y), (MARGIN + BOARD_PX, y), width)

            x = MARGIN + i * CELL_SIZE
            pygame.draw.line(self.screen, color, (x, MARGIN), (x, MARGIN + BOARD_PX), width)

        if self.last_move:
            row, col = self.last_move
            highlight = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            highlight.fill(C_HIGHLIGHT)
            self.screen.blit(highlight, (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE))

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                player = self.board.grid[row][col]
                if player == EMPTY:
                    continue

                cx, cy = self._px(row, col)
                radius = CELL_SIZE // 2 - 10

                if player == HUMAN:
                    offset = radius
                    pygame.draw.line(self.screen, C_X, (cx - offset, cy - offset), (cx + offset, cy + offset), 3)
                    pygame.draw.line(self.screen, C_X, (cx + offset, cy - offset), (cx - offset, cy + offset), 3)
                else:
                    pygame.draw.circle(self.screen, C_O, (cx, cy), radius, 3)

        if self.win_cells and len(self.win_cells) >= 2:
            pygame.draw.line(self.screen, C_WIN_LINE, self._px(*self.win_cells[0]), self._px(*self.win_cells[-1]), 5)
            for row, col in self.win_cells:
                pygame.draw.circle(self.screen, C_WIN_LINE, self._px(row, col), 6)

    def draw_info(self):
        panel_y = MARGIN * 2 + BOARD_PX
        pygame.draw.rect(self.screen, C_PANEL, pygame.Rect(0, panel_y, WIN_W, INFO_HEIGHT))
        pygame.draw.line(self.screen, C_GRID_BOLD, (0, panel_y), (WIN_W, panel_y), 1)

        x0, y0 = 18, panel_y + 12

        if self.game_over:
            if self.winner == HUMAN:
                message, color = "You win!  X WIN", C_STATUS_WIN
            elif self.winner == AI:
                message, color = "Computer wins!  O WIN", C_STATUS_LOSE
            else:
                message, color = "Draw!", C_STATUS_DRAW
        elif self.turn == HUMAN:
            message, color = "Your turn [X]", C_X
        else:
            message, color = "Computer thinking... [O]", C_O

        self.screen.blit(self.font_lg.render(message, True, color), (x0, y0))

        y0 += 32
        if stats["move"]:
            row, col = stats["move"]
            line1 = f"Move: ({row},{col})  Value: {stats['value']:+d}  Depth: {stats['depth']}"
            line2 = f"{self._mode_label()}: {stats['states']:,} states  {stats['time']:.3f}s"
            self.screen.blit(self.font_md.render(line1, True, C_TEXT), (x0, y0))
            self.screen.blit(self.font_md.render(line2, True, C_TEXT_DIM), (x0, y0 + 20))

            comparison = stats.get("comparison", {})
            mini = comparison.get("minimax")
            ab = comparison.get("alpha_beta")
            if mini and ab:
                line3 = (
                    f"MM: move {mini['move']}  val {mini['value']:+d}  "
                    f"states {mini['states']:,}  {mini['time']:.3f}s"
                )
                line4 = (
                    f"AB: move {ab['move']}  val {ab['value']:+d}  "
                    f"states {ab['states']:,}  cuts {ab['prunes']:,}  {ab['time']:.3f}s"
                )
                self.screen.blit(self.font_sm.render(line3, True, C_TEXT), (x0, y0 + 43))
                self.screen.blit(self.font_sm.render(line4, True, C_TEXT_DIM), (x0, y0 + 61))

        hint = f"X = Human   O = Computer   {WIN_COUNT} in a row wins"
        self.screen.blit(self.font_sm.render(hint, True, C_TEXT_DIM), (x0, panel_y + INFO_HEIGHT - 26))

        btn_w, btn_h = 150, 34
        btn_x = WIN_W - btn_w - 18
        self.mode_btn_rect = pygame.Rect(btn_x, panel_y + 18, btn_w, btn_h)
        self.btn_rect = pygame.Rect(btn_x, panel_y + 60, btn_w, btn_h)

        self._draw_button(self.mode_btn_rect, f"Mode: {self._mode_label()}")
        self._draw_button(self.btn_rect, "Restart [R]")

    def _mode_label(self):
        return "Alpha-Beta" if self.ai_mode == ALPHA_BETA else "Minimax"

    def _toggle_ai_mode(self):
        idx = AI_MODES.index(self.ai_mode)
        self.ai_mode = AI_MODES[(idx + 1) % len(AI_MODES)]
        stats["mode"] = self.ai_mode

    def _draw_button(self, rect, text):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_color = C_BTN_HOVER if rect.collidepoint(mouse_x, mouse_y) else C_BTN
        pygame.draw.rect(self.screen, button_color, rect, border_radius=6)
        pygame.draw.rect(self.screen, C_GRID_BOLD, rect, 1, border_radius=6)

        label = self.font_btn.render(text, True, C_BTN_TEXT)
        self.screen.blit(
            label,
            (
                rect.x + (rect.width - label.get_width()) // 2,
                rect.y + (rect.height - label.get_height()) // 2,
            ),
        )

    def _px(self, row, col):
        x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def _cell_from_mouse(self, mouse_x, mouse_y):
        col = (mouse_x - MARGIN) // CELL_SIZE
        row = (mouse_y - MARGIN) // CELL_SIZE
        return row, col

    def _finish_turn_if_needed(self, player):
        won, cells = self.board.check_win(player)
        if won:
            self.game_over = True
            self.winner = player
            self.win_cells = cells
            return True

        if self.board.is_full():
            self.game_over = True
            self.winner = None
            return True

        return False

    def run(self):
        ai_thinking = False

        while True:
            self.screen.fill(C_BG)
            self.draw_board()
            self.draw_info()
            pygame.display.flip()
            self.clock.tick(30)

            if not self.game_over and self.turn == AI and not ai_thinking:
                ai_thinking = True

                self.screen.fill(C_BG)
                self.draw_board()
                self.draw_info()
                pygame.display.flip()

                move = ai_move(self.board, self.ai_mode)
                if move:
                    row, col = move
                    self.board.place(row, col, AI)
                    self.last_move = (row, col)

                    if not self._finish_turn_if_needed(AI):
                        self.turn = HUMAN

                ai_thinking = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_m and not ai_thinking:
                        self._toggle_ai_mode()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos

                    if hasattr(self, "btn_rect") and self.btn_rect.collidepoint(mouse_x, mouse_y):
                        self.reset()
                        continue

                    if hasattr(self, "mode_btn_rect") and self.mode_btn_rect.collidepoint(mouse_x, mouse_y):
                        self._toggle_ai_mode()
                        continue

                    if not self.game_over and self.turn == HUMAN:
                        row, col = self._cell_from_mouse(mouse_x, mouse_y)
                        if self.board.is_valid(row, col) and self.board.grid[row][col] == EMPTY:
                            self.board.place(row, col, HUMAN)
                            self.last_move = (row, col)

                            if not self._finish_turn_if_needed(HUMAN):
                                self.turn = AI
