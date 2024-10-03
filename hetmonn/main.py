import pygame, os, time, random
pygame.init()  
pygame.mixer.init() 
pygame.font.init()  # Load font chữ

# Cài đặt cửa sổ game
WIDTH, HEIGHT = 700, 720  
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
ICON = pygame.image.load(os.path.join("anh", "pixel_ship_red_small.png")) 
pygame.display.set_icon(ICON)  # Đặt icon cho cửa sổ
pygame.display.set_caption("May bay chien dau by Hoang My")  

# Khởi tạo tàu địch
RED_SPACE_SHIP = pygame.image.load(os.path.join("anh", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("anh", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("anh", "pixel_ship_blue_small.png"))
PLANE_SHIP = pygame.image.load(os.path.join("anh", "plane.png"))  
# Khởi tạo tàu của người chơi
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("anh", "pixel_ship_yellow.png"))

# Khởi tạo laser
RED_LASER = pygame.image.load(os.path.join("anh", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("anh", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("anh", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("anh", "pixel_laser_yellow.png"))
PLANE_LASER = pygame.image.load(os.path.join("anh", "bullet.png"))

# Khởi tạo star và âm thanh
STAR_IMG = pygame.image.load(os.path.join("anh", "star.png"))
COLLECT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "sound-effect-twinklesparkle-115095.mp3"))
LASER_SOUND = pygame.mixer.Sound(os.path.join("sounds", "laser.wav"))

# Background game
BG = pygame.transform.scale(pygame.image.load(os.path.join("anh", "background.jpg")), (WIDTH, HEIGHT))

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
        return not (self.y <= height and self.y >= 0)

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
            LASER_SOUND.play()  # Play laser sound when shooting

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
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "plane": (PLANE_SHIP, PLANE_LASER)  # Add plane enemy
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.bullets_to_destroy = 3  

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def take_damage(self, damage):
        self.bullets_to_destroy -= damage

    def is_destroyed(self):
        return self.bullets_to_destroy <= 0

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = STAR_IMG
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

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
    stars = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 7
    laser_vel = 10
    high_score = get_high_score()

    player = Player(300, 630, point)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    timer_start = 20 

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))
        score_label = main_font.render(f"Score: {player.score}", True, (255, 255, 255))
        timer_label = main_font.render(f"Time Left: {int(timer_start)}s", True, (255, 255, 255))
        high_score_label = main_font.render(f"High Score: {high_score}", True, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (10, HEIGHT - score_label.get_height() - 10))
        WIN.blit(timer_label, (WIDTH / 2 - timer_label.get_width() / 2, 10))
        WIN.blit(high_score_label, (WIDTH - high_score_label.get_width() - 10, HEIGHT - high_score_label.get_height() - 10))

        for enemy in enemies:
            enemy.draw(WIN)

        for star in stars:
            star.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        timer_start -= 1 / FPS

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if timer_start <= 0: 
            level += 1
            timer_start = 20  
            wave_length += 5
            enemies.clear()

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

            for _ in range(random.randint(2, 5)):
                star = Star(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))
                stars.append(star)

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
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        for star in stars[:]:
            star.move(1)
            if star.off_screen(HEIGHT):
                stars.remove(star)
            elif star.collision(player):
                player.health = min(player.max_health, player.health + 10)  
                player.score += 55
                COLLECT_SOUND.play()  
                stars.remove(star)

        if player.score > high_score:
            high_score = player.score
            save_high_score(high_score)

        redraw_window()

def main_menu():
    title_font = pygame.font.SysFont(None, 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", True, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
