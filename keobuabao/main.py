import pygame
import random

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Keo Bua Bao Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)

buttons = {
    "keo": pygame.Rect(100, 400, 80, 40),
    "bua": pygame.Rect(200, 400, 80, 40),
    "bao": pygame.Rect(300, 400, 80, 40)
}

try:
    images = {
        "keo": pygame.transform.scale(pygame.image.load("keo.png"), (80, 80)),
        "bua": pygame.transform.scale(pygame.image.load("bua.png"), (80, 80)),
        "bao": pygame.transform.scale(pygame.image.load("bao.png"), (80, 80))
    }
except pygame.error as e:
    print(f"Khong the tai anh: {e}")
    pygame.quit()
    exit()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def determine_winner(nguoi_choi, may_choi):
    if nguoi_choi == may_choi:
        return "Hoa"
    elif (nguoi_choi == "keo"
          and may_choi == "bao") or (nguoi_choi == "bua" and may_choi
                                     == "keo") or (nguoi_choi == "bao"
                                                   and may_choi == "bua"):
        return "Ban thang"
    else:
        return "Ban thua"


def display_result(nguoi_choi, may_choi, ket_qua):
    screen.fill(WHITE)
    draw_text(f"Ban chon: {nguoi_choi}", font, BLACK, screen, 20, 20)
    draw_text(f"May chon: {may_choi}", font, BLACK, screen, 20, 60)
    draw_text(ket_qua, font, BLACK, screen, 20, 100)
    screen.blit(images[nguoi_choi], (20, 150))
    screen.blit(images[may_choi], (320, 150))


def game():
    running = True
    clock = pygame.time.Clock()
    nguoi_choi_choice = None
    may_choi_choice = None
    ket_qua = None

    while running:
        screen.fill(WHITE)

        for choice in buttons:
            pygame.draw.rect(screen,
                             RED if choice == nguoi_choi_choice else BLACK,
                             buttons[choice])
            draw_text(choice, font, WHITE, screen, buttons[choice].x + 10,
                      buttons[choice].y + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for choice in buttons:
                    if buttons[choice].collidepoint(event.pos):
                        nguoi_choi_choice = choice
                        may_choi_choice = random.choice(["keo", "bua", "bao"])
                        ket_qua = determine_winner(nguoi_choi_choice,
                                                   may_choi_choice)
                        break

        if nguoi_choi_choice and may_choi_choice and ket_qua:
            display_result(nguoi_choi_choice, may_choi_choice, ket_qua)
            pygame.display.update()
            pygame.time.wait(2000)
            nguoi_choi_choice = None
            may_choi_choice = None
            ket_qua = None

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


game()