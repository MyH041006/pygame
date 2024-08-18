import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước của cửa sổ
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Kích thước ô và bảng
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 2

# Bảng Sudoku (số 0 cho ô trống)
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def generate_initial_numbers(num_initial_cells=20):
    """Điền số ngẫu nhiên vào bảng Sudoku để bắt đầu."""
    for _ in range(num_initial_cells):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        num = random.randint(1, 9)
        if is_valid_move(row, col, num) and grid[row][col] == 0:
            grid[row][col] = num

def draw_grid():
    WIN.fill(WHITE)
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(WIN, BLACK, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(WIN, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), LINE_WIDTH)
    
    for x in range(0, GRID_SIZE + 1, 3):
        pygame.draw.line(WIN, BLACK, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE), LINE_WIDTH + 2)
        pygame.draw.line(WIN, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), LINE_WIDTH + 2)

def draw_numbers():
    font = pygame.font.SysFont(None, 40)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] != 0:
                text = font.render(str(grid[r][c]), True, BLACK)
                WIN.blit(text, (c * CELL_SIZE + CELL_SIZE // 3, r * CELL_SIZE + CELL_SIZE // 4))

def get_cell(pos):
    x, y = pos
    return x // CELL_SIZE, y // CELL_SIZE

def is_valid_move(row, col, num):
    # Kiểm tra hàng
    if num in grid[row]:
        return False

    # Kiểm tra cột
    for r in range(GRID_SIZE):
        if grid[r][col] == num:
            return False

    # Kiểm tra ô 3x3
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for r in range(box_row_start, box_row_start + 3):
        for c in range(box_col_start, box_col_start + 3):
            if grid[r][c] == num:
                return False

    return True

def main():
    run = True
    selected_cell = None

    # Điền số ngẫu nhiên vào bảng
    generate_initial_numbers(num_initial_cells=20)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Chọn ô khi nhấp chuột
                row, col = get_cell(event.pos)
                selected_cell = (row, col)
            elif event.type == pygame.KEYDOWN:
                # Nhập số khi có sự kiện bàn phím
                if selected_cell:
                    row, col = selected_cell
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                        num = event.key - pygame.K_0
                        if is_valid_move(row, col, num):
                            grid[row][col] = num
                        else:
                            print(f"Số {num} không hợp lệ tại ô ({row}, {col})")

        draw_grid()
        draw_numbers()
        pygame.display.update()

if __name__ == "__main__":
    main()
