import pygame
import random
import math

pygame.init()

# Mau sac
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (169, 169, 169)
gold = (255, 215, 0)
purple = (160, 32, 240)

# Man hinh
screen_width = 450
screen_height = 450
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Dong ho
clock = pygame.time.Clock()

# Thong so ran
snake_block = 25
initial_snake_speed = 15
snake_speed = initial_snake_speed

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Ve ran
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

# Hien thi diem
def display_score(score, level):
    value = score_font.render("Diem cua ban: " + str(score) + " Level: " + str(level), True, yellow)
    screen.blit(value, [0, 0])

# Hien thi thong bao
def display_message(msg, color, position):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, position)

# Thanh truot toc do
def draw_speed_slider(speed):
    pygame.draw.rect(screen, gray, [50, screen_height - 50, 350, 10])
    pygame.draw.rect(screen, black, [50 + (speed - 1) * 35, screen_height - 60, 20, 30])
    label = font_style.render(f"Toc do: {speed}", True, black)
    screen.blit(label, [screen_width - 150, screen_height - 80])

# Kiem tra su va cham
def check_collision(x1, y1, obj_x, obj_y, size):
    return (x1 < obj_x + size and x1 + snake_block > obj_x and y1 < obj_y + size and y1 + snake_block > obj_y)

# Ve chuong ngai vat
def draw_obstacles(obstacles):
    for obs in obstacles:
        shape, x, y = obs
        if shape == 'square':
            pygame.draw.rect(screen, red, [x, y, snake_block, snake_block])
        elif shape == 'triangle':
            pygame.draw.polygon(screen, red, [(x, y), (x + snake_block, y), (x + snake_block / 2, y - snake_block)])

# Tao chuong ngai vat
def create_obstacles(num_obstacles):
    obstacles = []
    shapes = ['square', 'triangle']
    for _ in range(num_obstacles):
        shape = random.choice(shapes)
        obs_x = round(random.randrange(0, screen_width - snake_block) / 25.0) * 25.0
        obs_y = round(random.randrange(0, screen_height - snake_block) / 25.0) * 25.0
        if shape == 'triangle':
            obs_y += snake_block  # Điều chỉnh tọa độ y cho tam giác để vẽ đúng vị trí
        obstacles.append((shape, obs_x, obs_y))
    return obstacles

# Kiem tra va cham voi chuong ngai vat
def check_obstacle_collision(x1, y1, obstacles):
    for obs in obstacles:
        shape, obs_x, obs_y = obs
        if shape == 'square':
            if check_collision(x1, y1, obs_x, obs_y, snake_block):
                return True
        elif shape == 'triangle':
            # Kiem tra va cham tam giac
            if check_collision(x1, y1, obs_x, obs_y - snake_block, snake_block):
                return True
    return False

# Vong lap chinh
def game_loop():
    global snake_speed

    game_over = False
    game_close = False
    adjust_speed = True
    level_up_message = False
    invalid_key_message = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 25.0) * 25.0
    foody = round(random.randrange(0, screen_height - snake_block) / 25.0) * 25.0

    foods = [[foodx, foody]]

    special_food_active = False
    special_food_timer = 0
    special_foodx = 0
    special_foody = 0

    obstacles = create_obstacles(5)  # Them chuong ngai vat
    food_count = 0  # Dem so luong thuc an da an

    level = 1

    while not game_over:
        while game_close:
            screen.fill(blue)
            display_message("Ban thua! Nhan C de choi lai hoac Q de thoat", red, (screen_width / 6, screen_height / 3))
            display_score(snake_length - 1, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                else:
                    invalid_key_message = True
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000, loops=1)  # Hien thong bao trong 1 giay

            # Dieu chinh thanh truot toc do
            if event.type == pygame.MOUSEBUTTONDOWN and adjust_speed:
                if 50 <= event.pos[0] <= 400 and screen_height - 60 <= event.pos[1] <= screen_height - 30:
                    snake_speed = (event.pos[0] - 50) // 35 + 1
                    adjust_speed = False

            if event.type == pygame.USEREVENT + 1:
                invalid_key_message = False

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)

        for food in foods:
            pygame.draw.ellipse(screen, green, [food[0], food[1], snake_block, snake_block])

        if special_food_active:
            pygame.draw.ellipse(screen, gold, [special_foodx, special_foody, snake_block, snake_block])
            special_food_timer -= 1
            if special_food_timer <= 0:
                special_food_active = False

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        if check_obstacle_collision(x1, y1, obstacles):
            game_close = True

        draw_snake(snake_block, snake_list)
        display_score(snake_length - 1, level)
        draw_obstacles(obstacles)

        if adjust_speed:
            draw_speed_slider(snake_speed)

        if level_up_message:
            display_message("Level Up!", yellow, (screen_width / 3, screen_height / 4))

        if invalid_key_message:
            display_message("Invalid Key!", red, (screen_width / 3, screen_height / 2))

        pygame.display.update()

        # Kiem tra su va cham voi thuc an
        for food in foods:
            if check_collision(x1, y1, food[0], food[1], snake_block):
                foods.remove(food)
                snake_length += 1
                food_count += 1
                break

        if not foods:
            foodx = round(random.randrange(0, screen_width - snake_block) / 25.0) * 25.0
            foody = round(random.randrange(0, screen_height - snake_block) / 25.0) * 25.0
            foods.append([foodx, foody])

        if special_food_active and check_collision(x1, y1, special_foodx, special_foody, snake_block):
            special_food_active = False
            snake_length += 5  # Tang do dai cua ran len 5 khi an thuc an dac biet

        # Xuat hien ngau nhien thuc an dac biet
        if not special_food_active and random.randint(1, 50) == 1:
            special_foodx = round(random.randrange(0, screen_width - snake_block) / 25.0) * 25.0
            special_foody = round(random.randrange(0, screen_height - snake_block) / 25.0) * 25.0
            special_food_active = True
            special_food_timer = 10  # Thoi gian ton tai cua thuc an dac biet

        # Tang level
        if food_count >= 10:
            food_count = 0
            level += 1
            snake_speed += 3  # Tang toc do ran khi tang level
            level_up_message = True
            pygame.time.set_timer(pygame.USEREVENT + 2, 1000, loops=1)  # Hien thong bao trong 1 giay

        if event.type == pygame.USEREVENT + 2:
            level_up_message = False

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
