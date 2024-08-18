import pygame
import random
import os

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
screen_width = 400
screen_height = 450
screen = pygame.display.set_mode((screen_width, screen_height))

# Tải hình ảnh
bird_image = pygame.image.load('bird.png')
pipe_image = pygame.image.load('column.png')
background_image = pygame.image.load('background.png')

# Thay đổi kích thước hình ảnh ống
pipe_image = pygame.transform.scale(pipe_image, (60, 300))  # Thay đổi kích thước ống (width, height)

# Tải âm thanh
point_sound = pygame.mixer.Sound('coin-recieved-230517.mp3')
hit_sound = pygame.mixer.Sound('attention-179098.mp3')

# Phông chữ để hiển thị điểm số và văn bản
font = pygame.font.SysFont(None, 35)
large_font = pygame.font.SysFont(None, 75)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.velocity = 0
        self.gravity = 0.4  # Giảm trọng lực để chim rơi chậm hơn
        self.jump_strength = -7  # Giảm tốc độ nhảy để chim nhảy vừa phải

    def draw(self, screen):
        screen.blit(bird_image, (self.x, self.y))

    def update(self):
        self.y += self.velocity
        self.velocity += self.gravity

    def jump(self):
        self.velocity = self.jump_strength  # Áp dụng tốc độ nhảy mới

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap = 150  # Khoảng cách giữa ống trên và ống dưới
        self.upper_height = random.randint(50, screen_height - self.gap - 50)  # Chiều cao ngẫu nhiên cho ống trên
        self.lower_height = screen_height - self.upper_height - self.gap  # Tính chiều cao của ống dưới
        self.speed = 2  # Tốc độ di chuyển của các ống

    def move(self):
        self.x -= self.speed

    def draw(self, screen):
        # Vẽ ống trên
        screen.blit(pygame.transform.scale(pipe_image, (60, self.upper_height)), (self.x, 0))  # Ống trên bắt đầu từ đỉnh
        # Vẽ ống dưới
        screen.blit(pygame.transform.scale(pipe_image, (60, self.lower_height)), (self.x, screen_height - self.lower_height))  # Ống dưới bắt đầu từ đáy

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = [Pipe(screen_width + i * 226) for i in range(5)]  # Khoảng cách giữa các cột
        self.score = 0
        self.high_score = self.load_high_score()
        self.paused = False
        self.game_over = False
        self.started = False
        self.play_again_button = None
        self.quit_button = None

    def load_high_score(self):
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not self.started:
                        self.started = True
                    elif not self.game_over:
                        self.bird.jump()
                if event.key == pygame.K_p and self.started:
                    self.paused = not self.paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.started:
                    self.started = True
                elif self.game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_again_button and self.play_again_button.collidepoint(mouse_pos):
                        self.reset_game()
                    elif self.quit_button and self.quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        quit()
                else:
                    self.bird.jump()

    def check_collision(self):
        bird_rect = pygame.Rect(self.bird.x, self.bird.y, bird_image.get_width(), bird_image.get_height())
        for pipe in self.pipes:
            pipe_rect_top = pygame.Rect(pipe.x, 0, 60, pipe.upper_height)  # Rect cho ống trên
            pipe_rect_bottom = pygame.Rect(pipe.x, screen_height - pipe.lower_height, 60, pipe.lower_height)  # Rect cho ống dưới
            if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
                return True
        return False

    def show_score(self, screen):
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

    def show_game_over(self, screen):
        game_over_text = large_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))

        button_width = max(font.size("Play Again")[0], 200)  # Kích thước nút đủ chứa chữ
        button_height = 50
        button_spacing = int(2 * (screen_height / 15))  # Khoảng cách 2cm giữa các nút

        play_again_text = font.render("Play Again", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))

        self.play_again_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 50, button_width, button_height)
        self.quit_button = pygame.Rect(screen_width // 2 - button_width // 2, self.play_again_button.bottom + button_spacing, button_width, button_height)

        pygame.draw.rect(screen, (0, 255, 0), self.play_again_button)
        pygame.draw.rect(screen, (255, 0, 0), self.quit_button)

        screen.blit(play_again_text, (self.play_again_button.x + (button_width - play_again_text.get_width()) // 2, self.play_again_button.y + (button_height - play_again_text.get_height()) // 2))
        screen.blit(quit_text, (self.quit_button.x + (button_width - quit_text.get_width()) // 2, self.quit_button.y + (button_height - quit_text.get_height()) // 2))

    def show_start_screen(self, screen):
        start_text = large_font.render("Start Game", True, (0, 0, 0))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - start_text.get_height() // 2))

    def reset_game(self):
        self.bird = Bird()
        self.pipes = [Pipe(screen_width + i * 226) for i in range(5)]  # Đặt lại khoảng cách giữa các cột
        self.score = 0
        self.game_over = False

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.handle_input()

            if not self.started:
                screen.blit(background_image, (0, 0))
                self.show_start_screen(screen)
            elif self.game_over:
                screen.blit(background_image, (0, 0))
                self.show_game_over(screen)
            else:
                if not self.paused:
                    self.bird.update()
                    for pipe in self.pipes:
                        pipe.move()
                    # Xóa ống khi nó ra khỏi màn hình và thêm ống mới vào danh sách
                    if self.pipes[0].x < -pipe_image.get_width():
                        self.pipes.pop(0)
                        new_pipe = Pipe(self.pipes[-1].x + 226)  # Đảm bảo khoảng cách giữa các cột
                        self.pipes.append(new_pipe)
                        self.score += 1
                        point_sound.play()
                        self.update_high_score()

                    if self.check_collision() or self.bird.y > screen_height or self.bird.y < 0:
                        hit_sound.play()
                        self.game_over = True

                screen.blit(background_image, (0, 0))
                self.bird.draw(screen)
                for pipe in self.pipes:
                    pipe.draw(screen)
                self.show_score(screen)

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run()
