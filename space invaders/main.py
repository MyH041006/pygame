# Import các thư viện cần thiết
import pygame, os, time, random
pygame.font.init()  # Load font chữ

# Cài đặt cửa sổ game
WIDTH, HEIGHT = 700, 700  # Chiều rộng và chiều cao của cửa sổ
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Khởi tạo cửa sổ
ICON = pygame.image.load(os.path.join("anh", "pixel_ship_red_small.png"))  # Icon cho cửa sổ
pygame.display.set_icon(ICON)  # Đặt icon cho cửa sổ
pygame.display.set_caption("Space Invaders")  # Đặt tên cho cửa sổ game

# Khởi tạo tàu địch
RED_SPACE_SHIP = pygame.image.load(os.path.join("anh", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("anh", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("anh", "pixel_ship_blue_small.png"))

# Khởi tạo tàu của người chơi
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("anh", "pixel_ship_yellow.png"))

# Khởi tạo laser
RED_LASER = pygame.image.load(os.path.join("anh", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("anh", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("anh", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("anh", "pixel_laser_yellow.png"))

# Background game
BG = pygame.transform.scale(pygame.image.load(os.path.join("anh", "background-black.png")), (WIDTH, HEIGHT))

# Class cho laser với 4 phương thức: draw(), move(), off_screen(), collision()
class Laser:
    def __init__(self, x, y, img):  # Hàm khởi tạo
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

# Class cho tàu
class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, point, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0
        self.point = point

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        self.score += self.point
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def get_high_score():
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    point = 100
    main_font = pygame.font.SysFont(None, 40)
    lost_font = pygame.font.SysFont(None, 50)
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 7
    laser_vel = 10
    high_score = get_high_score()

    player = Player(300, 630, point)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"{lives} Mang", 1, (255, 255, 255))
        level_label = main_font.render(f"Level {level}", 1, (255, 255, 255))
        score_label = main_font.render(f"Diem: {int(player.score)}", 1, (255, 255, 255))
        high_score_label = main_font.render(f"Diem cao nhat: {high_score}", 1, (255, 255, 255))
        enemies_label = main_font.render(f"Con {len(enemies)} dich", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (10, 60))
        WIN.blit(high_score_label, (10, 110))
        WIN.blit(enemies_label, (WIDTH - enemies_label.get_width() - 10, 60))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Ban da thua", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 275))
            final_score_label = lost_font.render(f"Diem dat duoc: {player.score}", 1, (0, 255, 255))
            WIN.blit(final_score_label, (WIDTH / 2 - final_score_label.get_width() / 2, 325))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if player.score > high_score:
                save_high_score(player.score)
                high_score = player.score
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

def main_menu():
    title_font = pygame.font.SysFont(None, 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title = title_font.render("Bam de choi...", 1, (255, 255, 255))
        WIN.blit(title, (WIDTH / 2 - title.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
