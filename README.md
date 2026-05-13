"""
README - Hướng dẫn sử dụng trò chơi Cờ Caro AI
Caro Game with Pure Minimax AI - User Guide
"""

# ═══════════════════════════════════════════════════════════════════
#                       CỬ CẢ TRƠNG CARO AI
#             CARO GAME WITH PURE MINIMAX AI (LEVEL 1)
# ═══════════════════════════════════════════════════════════════════

## 📋 MÔ TẢ DỰ ÁN / PROJECT DESCRIPTION

Đây là trò chơi Cờ Caro (Gomoku) với AI thông minh sử dụng thuật toán Minimax thuần túy.
Người chơi (X - xanh lam) đối đầu với máy tính (O - đỏ). Thắng khi có 4 quân liên tiếp.

This is a Caro (Gomoku) game where you play against an AI powered by the Pure Minimax algorithm.
You play as X (light blue) against the computer (O - red). Win by getting 4 in a row.

---

## 🗂️ CẤU TRÚC TỆP / FILE STRUCTURE

```
Python_caro_AI/
├── config.py          # Cấu hình, hằng số, màu sắc
├── board.py           # Lớp Board - quản lý trạng thái bàn cờ
├── evaluation.py      # Hàm đánh giá trạng thái (heuristic)
├── minimax.py         # Thuật toán Minimax cho AI
├── game.py            # Giao diện Pygame chính
├── main.py            # Điểm khởi đầu (entry point)
├── requirements.txt   # Danh sách thư viện cần cài
└── README.md          # File này
```

### 📄 Chi tiết từng file:

**config.py**
- Cấu hình: kích thước bàn cờ (9x9), độ sâu Minimax (3 nước)
- Bảng màu RGB cho giao diện (nền, lưới, quân, text)
- Hằng số: EMPTY, HUMAN, AI

**board.py**
- Lớp `Board`: quản lý lưới, quân cờ
- Phương thức:
  - `place(r, c, player)`: Đặt quân
  - `undo()`: Hoàn tác
  - `check_win(player)`: Kiểm tra thắng
  - `get_candidates()`: Lấy nước đi ứng cử viên
  - `_count_dir()`: Đếm quân liên tiếp

**evaluation.py**
- `score_line()`: Cho điểm một đoạn quân (ví dụ: 3 quân + 2 đầu mở = 5000 điểm)
- `evaluate()`: Đánh giá toàn bàn cờ (cộng điểm tất cả đoạn quân)

**minimax.py**
- `minimax()`: Đệ quy tìm nước đi tối ưu (maximizing vs minimizing)
- `ai_move()`: Chọn nước đi tốt nhất cho AI
- `stats`: Thống kê (số nút xét, thời gian, giá trị)

**game.py**
- Lớp `Game`: quản lý vòng lặp trò chơi chính
- Phương thức:
  - `draw_board()`: Vẽ bàn cờ và quân
  - `draw_info()`: Vẽ panel thông tin
  - `run()`: Vòng lặp chính

**main.py**
- Hàm `main()`: Khởi tạo Pygame và chạy trò chơi

---

## 🚀 CÁCH CHẠY / HOW TO RUN

### Bước 1: Cài đặt Python 3.8+
```bash
# Kiểm tra phiên bản Python
python --version
```

### Bước 2: Cài đặt thư viện
```bash
# Cài đặt từ requirements.txt
pip install -r requirements.txt
```

### Bước 3: Chạy trò chơi
```bash
python main.py
```

---

## 🎮 CÁCH CHƠI / HOW TO PLAY

- **Lượt của bạn**: Click vào bất kỳ ô trống nào để đặt quân X
- **Lượt máy**: Máy sẽ tự động tính toán và đặt quân O
- **Thắng**: Là người đầu tiên đạt 4 quân liên tiếp (ngang, dọc, chéo)
- **Chơi lại**: Nhấn nút "Chơi lại [R]" hoặc phím R

---

## 🧠 THUẬT TOÁN MINIMAX / MINIMAX ALGORITHM

Minimax là một thuật toán tìm kiếm:

```
Maximizing Player (AI) ← Tìm nước đi tốt (điểm cao)
  ↓
Đệ quy với độ sâu = MAX_DEPTH (3 nước)
  ↓
Minimizing Player (Người chơi) ← Giả sử tìm nước đi xấu (điểm thấp) cho AI
  ↓
Lặp lại → Tìm nước đi tối ưu bằng cách xem tổ hợp có thể
```

**Ưu điểm:**
- Đơn giản, dễ hiểu
- Tính toán tương đối nhanh với độ sâu 3

**Nhược điểm:**
- Không có Alpha-Beta Pruning (tối ưu hóa)
- Độ sâu 3 là giới hạn (nếu tăng sẽ quá chậm)

---

## 📊 HỆ THỐNG ĐIỂM / SCORING SYSTEM

Cách AI đánh giá trạng thái bàn cờ:

| Tình huống                      | Điểm     | Mô tả                           |
|--------------------------------|---------|--------------------------------|
| AI 4 quân liên tiếp (thắng)    | +100,000| Trạng thái thắng               |
| AI 3 quân + 2 đầu mở          | +5,000  | Rất nguy hiểm                 |
| AI 3 quân + 1 đầu mở          | +500    | Nguy hiểm vừa                 |
| AI 2 quân + 2 đầu mở          | +100    | Có tiềm năng                  |
| Người 3 quân + 2 đầu mở       | -10,000 | Cần chặn ngay                 |
| Người 3 quân + 1 đầu mở       | -1,000  | Nên chặn                      |

Lưu ý: Chặn người chơi được ưu tiên cao hơn (nhân 2) so với bắt được

---

## ⚙️ TUNING & TỐI ƯU HÓA / CONFIGURATION

Bạn có thể chỉnh các tham số trong `config.py`:

```python
BOARD_SIZE = 9      # Kích thước bàn (mặc định 9x9)
WIN_COUNT = 4       # Số quân để thắng (mặc định 4)
MAX_DEPTH = 3       # Độ sâu Minimax (3 = vừa phải)
                    # Tăng lên → AI mạnh hơn nhưng chậm hơn
                    # Giảm xuống → AI yếu hơn nhưng nhanh hơn
```

Nếu chỉnh `MAX_DEPTH`:
- `2`: Rất nhanh, nhưng AI yếu
- `3`: Cân bằng (mặc định)
- `4`: AI mạnh hơn nhưng chậm (1-2 giây mỗi nước)
- `5+`: Quá chậm, không khuyến cáo

---

## 📝 GIẢI THÍCH MÃ / CODE WALKTHROUGH

### Ví dụ 1: Kiểm tra thắng

```python
# Trong board.py
def check_win(self, player):
    # Duyệt mỗi ô trên bàn
    for r in range(self.size):
        for c in range(self.size):
            # Kiểm tra 4 hướng từ ô này
            for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
                # Đếm quân liên tiếp
                count = 1 + count_forward + count_backward
                # Nếu >= 4, player thắng
                if count >= WIN_COUNT:
                    return True, cells_list
```

### Ví dụ 2: Minimax đệ quy

```python
# Trong minimax.py
def minimax(board, depth, is_maximizing):
    # Cơ sở: kiểm tra trạng thái kết thúc
    if board.check_win(AI):
        return SCORE_WIN + depth  # Thắng sớm hơn tốt hơn
    if depth == 0:
        return evaluate(board)
    
    # Đệ quy
    if is_maximizing:  # AI đi
        best = -inf
        for move in candidates:
            board.place(move, AI)
            val = minimax(board, depth - 1, False)  # Người đi tiếp
            board.undo()
            best = max(best, val)
    else:  # Người chơi đi
        best = +inf
        for move in candidates:
            board.place(move, HUMAN)
            val = minimax(board, depth - 1, True)  # AI đi tiếp
            board.undo()
            best = min(best, val)
    return best
```

---

## 🐛 TROUBLESHOOTING

**Lỗi: "ModuleNotFoundError: No module named 'pygame'"**
```bash
pip install pygame
```

**Trò chơi chạy rất chậm**
- Giảm `MAX_DEPTH` từ 3 xuống 2 trong `config.py`

**AI không đánh**
- Kiểm tra console xem có lỗi gì không
- Thử chạy lại trò chơi

---

## 📚 TÀI LIỆU THAM KHẢO / REFERENCES

- Minimax Algorithm: https://en.wikipedia.org/wiki/Minimax
- Pygame Documentation: https://www.pygame.org/docs/
- Gomoku Rules: https://en.wikipedia.org/wiki/Gomoku

---

## 📝 GHI CHÚ / NOTES

- Mã nguồn có ghi chú tiếng Việt chi tiết
- Tất cả hàm có docstring giải thích
- Dễ mở rộng: thêm Alpha-Beta Pruning, lưu trữ transposition table, v.v.

---

## 👨‍💻 PHÁT TRIỂN TIẾP THEO / FUTURE IMPROVEMENTS

- [ ] Alpha-Beta Pruning (tối ưu hóa Minimax)
- [ ] Transposition Table (lưu trữ kết quả đã tính)
- [ ] Difficulty Level (dễ, trung bình, khó)
- [ ] Time Control (giới hạn thời gian suy nghĩ)
- [ ] Undo/Redo (hoàn tác/làm lại nước đi)
- [ ] Multiplayer (hai người chơi)

---

**Tác giả: Caro AI Project**  
**Phiên bản: 1.0**  
**Ngày: 2026**
