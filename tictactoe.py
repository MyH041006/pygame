import pygame
import sys

pygame.init()

# Các hằng số
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
X_COLOR = (28, 170, 156)
O_COLOR = (239, 231, 200)
BG_COLOR = (0, 0, 0)
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Khởi tạo cửa sổ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Bảng trò chơi
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_board():
    screen.fill(BOARD_COLOR)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_marks():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            mark = board[row][col]
            if mark:
                color = X_COLOR if mark == 'X' else O_COLOR
                font = pygame.font.Font(None, 74)
                text = font.render(mark, True, color)
                text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(text, text_rect)

def check_winner():
    # Kiểm tra hàng và cột
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    # Kiểm tra đường chéo
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def check_draw():
    return all(board[row][col] is not None for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def minimax(board, is_maximizing):
    winner = check_winner()
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif check_draw():
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    score = minimax(board, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    score = minimax(board, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = float('-inf')
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'O'
                score = minimax(board, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        board[best_move[0]][best_move[1]] = 'O'

def main():
    current_player = 'X'
    running = True

    while running:
        draw_board()
        draw_marks()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_player == 'X':
                    x, y = event.pos
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    if board[row][col] is None:
                        board[row][col] = current_player
                        if check_winner():
                            print(f'Người chơi {current_player} thắng!')
                            running = False
                        elif check_draw():
                            print('Hòa!')
                            running = False
                        current_player = 'O'

        if current_player == 'O' and running:
            ai_move()
            if check_winner():
                print('AI thắng!')
                running = False
            elif check_draw():
                print('Hòa!')
                running = False
            current_player = 'X'

    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()
