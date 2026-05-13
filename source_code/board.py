"""
Lớp Board và logic bàn cờ
Board class and game board logic
"""

from config import BOARD_SIZE, WIN_COUNT, EMPTY, HUMAN, AI


class Board:
    """
    Lớp quản lý trạng thái bàn cờ.
    
    Board class manages the game state:
    - Lưu trữ trạng thái các ô
    - Kiểm tra thắng/hòa
    - Quản lý lịch sử nước đi
    """

    def __init__(self, size=BOARD_SIZE):
        """
        Khởi tạo bàn cờ trống.
        
        Args:
            size: Kích thước bàn cờ (mặc định 9x9)
        """
        self.size = size
        # Lưới chứa giá trị: EMPTY (0), HUMAN (1), hoặc AI (2)
        self.grid = [[EMPTY] * size for _ in range(size)]
        # Lịch sử các nước đi: danh sách (row, col, player)
        self.moves = []

    def copy(self):
        """
        Tạo bản sao độc lập của bàn cờ.
        Dùng khi cần mô phỏng nước đi trong thuật toán Minimax.
        
        Returns:
            Board: Bàn cờ mới với cùng trạng thái
        """
        b = Board(self.size)
        # Copy lưới
        b.grid = [row[:] for row in self.grid]
        # Copy lịch sử
        b.moves = self.moves[:]
        return b

    def is_valid(self, r, c):
        """
        Kiểm tra ô có nằm trong bàn cờ hay không.
        
        Args:
            r, c: Tọa độ hàng và cột
            
        Returns:
            bool: True nếu tọa độ hợp lệ, False nếu ngoài bàn cờ
        """
        return 0 <= r < self.size and 0 <= c < self.size

    def place(self, r, c, player):
        """
        Đặt quân của người chơi tại vị trí (r, c).
        
        Args:
            r, c: Tọa độ hàng và cột
            player: Người chơi (HUMAN hoặc AI)
            
        Returns:
            bool: True nếu đặt thành công, False nếu ô đã có quân
        """
        # Kiểm tra ô có trống không
        if self.grid[r][c] != EMPTY:
            return False
        
        # Đặt quân
        self.grid[r][c] = player
        # Ghi lại nước đi
        self.moves.append((r, c, player))
        return True

    def undo(self):
        """
        Hoàn tác nước đi cuối cùng (loại bỏ quân vừa đặt).
        Dùng trong thuật toán Minimax để thử các nước đi.
        
        Returns:
            None
        """
        if self.moves:
            r, c, _ = self.moves.pop()
            self.grid[r][c] = EMPTY

    def is_full(self):
        """
        Kiểm tra bàn cờ đã đầy chưa (hòa).
        
        Returns:
            bool: True nếu tất cả ô đã được đánh
        """
        return all(self.grid[r][c] != EMPTY
                   for r in range(self.size) for c in range(self.size))

    def _count_dir(self, r, c, dr, dc, player):
        """
        Đếm số quân liên tiếp của người chơi theo một hướng.
        Hướng được xác định bởi (dr, dc).
        
        Args:
            r, c: Vị trí bắt đầu
            dr, dc: Hướng (0,1)=ngang, (1,0)=dọc, (1,1)=chéo /, (1,-1)=chéo \\
            player: Người chơi để kiểm tra
            
        Returns:
            int: Số quân liên tiếp theo hướng đó
        """
        count = 0
        nr, nc = r + dr, c + dc
        # Đếm liên tiếp cho đến khi gặp ô không phải của player
        while self.is_valid(nr, nc) and self.grid[nr][nc] == player:
            count += 1
            nr += dr
            nc += dc
        return count

    def check_win(self, player):
        """
        Kiểm tra xem người chơi đã thắng hay chưa.
        Trả về vị trí các quân tạo thành đường thắng nếu có.
        
        Args:
            player: Người chơi để kiểm tra (HUMAN hoặc AI)
            
        Returns:
            tuple: (is_win, cells)
                - is_win: True/False
                - cells: Danh sách tọa độ (r, c) tạo thành đường thắng
        """
        # 4 hướng: ngang, dọc, chéo /, chéo \\
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        # Duyệt từng ô trên bàn cờ
        for r in range(self.size):
            for c in range(self.size):
                # Bỏ qua ô không phải của player
                if self.grid[r][c] != player:
                    continue
                
                # Kiểm tra 4 hướng từ ô này
                for dr, dc in dirs:
                    # Đếm quân liên tiếp theo hướng (dr, dc)
                    cnt_forward = self._count_dir(r, c, dr, dc, player)
                    # Đếm quân liên tiếp theo hướng ngược lại
                    cnt_backward = self._count_dir(r, c, -dr, -dc, player)
                    # Tổng cộng (bao gồm ô hiện tại)
                    total = 1 + cnt_forward + cnt_backward
                    
                    # Nếu >= WIN_COUNT (mặc định 4), player thắng
                    if total >= WIN_COUNT:
                        # Thu thập ô tạo thành đường thắng
                        cells = [(r, c)]
                        
                        # Thêm ô phía trước
                        nr, nc = r + dr, c + dc
                        while self.is_valid(nr, nc) and self.grid[nr][nc] == player:
                            cells.append((nr, nc))
                            nr += dr
                            nc += dc
                        
                        # Thêm ô phía sau
                        nr, nc = r - dr, c - dc
                        while self.is_valid(nr, nc) and self.grid[nr][nc] == player:
                            cells.append((nr, nc))
                            nr -= dr
                            nc -= dc
                        
                        return True, cells
        
        return False, []

    def get_candidates(self):
        """
        Lấy danh sách các ô ứng cử viên để đánh tiếp.
        Tối ưu hóa: chỉ xét các ô lân cận những ô đã được đánh.
        
        Returns:
            list: Danh sách tọa độ (r, c) là ứng cử viên
        """
        # Nếu bàn cờ trống, trả về tâm bàn cờ
        if not self.moves:
            mid = self.size // 2
            return [(mid, mid)]
        
        # Tập hợp ô đã được đánh
        occupied = {(r, c) for r, c, _ in self.moves}
        
        # Tập hợp ô ứng cử viên (xung quanh ô đã đánh)
        candidates = set()
        for r, c, _ in self.moves:
            # Xét các ô trong bán kính 2 xung quanh (r, c)
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    nr, nc = r + dr, c + dc
                    # Nếu ô hợp lệ và trống, thêm vào ứng cử viên
                    if self.is_valid(nr, nc) and (nr, nc) not in occupied:
                        candidates.add((nr, nc))
        
        return list(candidates)
