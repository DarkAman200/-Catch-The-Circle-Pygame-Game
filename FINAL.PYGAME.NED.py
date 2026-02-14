import pygame
import random
import sys

pygame.init()
clock = pygame.time.Clock()

# -------------------- SETTINGS --------------------
WIDTH, HEIGHT = 500, 400
FPS = 60
MAX_LIVES = 3

CIRCLE_SIZE = 30
RECT_W, RECT_H = 80, 20
RECT_SPEED = 7

BASE_CIRCLE_SPEED = 3
POWERUP_LIMIT = 2
SLOW_DURATION = 180  # frames (~3 seconds)

# -------------------- COLORS --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 200, 0)

# -------------------- SCREEN --------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Circle - Arcade Edition")

# -------------------- FONTS --------------------
font = pygame.font.SysFont("arial", 16)
big_font = pygame.font.SysFont("arial", 32)

# -------------------- HELPERS --------------------
def draw_text(text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
    screen.blit(surf, rect)

def reset_circle(level):
    return {
        "rect": pygame.Rect(
            random.randint(0, WIDTH - CIRCLE_SIZE),
            -CIRCLE_SIZE,
            CIRCLE_SIZE,
            CIRCLE_SIZE
        ),
        "speed": BASE_CIRCLE_SPEED + level
    }

def reset_powerup():
    return {
        "rect": pygame.Rect(
            random.randint(0, WIDTH - 30),
            -30,
            30,
            30
        ),
        "type": random.choice(["life", "slow"]),
        "speed": 4
    }

def reset_game():
    return {
        "player": pygame.Rect(WIDTH//2 - RECT_W//2, HEIGHT - 40, RECT_W, RECT_H),
        "score": 0,
        "missed": 0,
        "lives": MAX_LIVES,
        "level": 0,
        "paused": False,
        "slow_timer": 0,
        "circle": reset_circle(0),
        "powerups": []
    }

# -------------------- SCREENS --------------------
def start_screen():
    while True:
        clock.tick(30)
        screen.fill(WHITE)
        draw_text("Catch The Circle", big_font, BLACK, WIDTH//2, 150, True)
        draw_text("Press SPACE to Start", font, BLACK, WIDTH//2, 210, True)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                return

def game_over_screen(score, missed):
    while True:
        clock.tick(30)
        screen.fill(WHITE)
        draw_text("GAME OVER", big_font, RED, WIDTH//2, 120, True)
        draw_text(f"Score: {score}", font, BLACK, WIDTH//2, 170, True)
        draw_text(f"Missed: {missed}", font, BLACK, WIDTH//2, 195, True)
        draw_text("R = Restart   Q = Quit", font, BLACK, WIDTH//2, 240, True)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return
                if e.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# -------------------- GAME LOOP --------------------
start_screen()
game = reset_game()
running = True

while running:
    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
            game["paused"] = not game["paused"]

    if game["paused"]:
        screen.fill(WHITE)
        draw_text("PAUSED", big_font, BLACK, WIDTH//2, HEIGHT//2, True)
        draw_text("Press P to Resume", font, BLACK, WIDTH//2, HEIGHT//2 + 40, True)
        pygame.display.update()
        continue

    # ----- INPUT -----
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game["player"].x -= RECT_SPEED
    if keys[pygame.K_RIGHT]:
        game["player"].x += RECT_SPEED
    game["player"].x = max(0, min(game["player"].x, WIDTH - RECT_W))

    # ----- CIRCLE -----
    circle = game["circle"]
    speed = circle["speed"] - (1 if game["slow_timer"] > 0 else 0)
    circle["rect"].y += max(1, speed)

    if game["player"].colliderect(circle["rect"]):
        game["score"] += 1
        if game["score"] % 5 == 0:
            game["level"] += 1
        game["circle"] = reset_circle(game["level"])

    elif circle["rect"].top > HEIGHT:
        game["missed"] += 1
        game["lives"] -= 1
        game["circle"] = reset_circle(game["level"])

        if len(game["powerups"]) < POWERUP_LIMIT and random.random() < 0.4:
            game["powerups"].append(reset_powerup())

        if game["lives"] <= 0:
            game_over_screen(game["score"], game["missed"])
            game = reset_game()
            continue

    # ----- POWERUPS -----
    for pu in game["powerups"][:]:
        pu["rect"].y += pu["speed"]

        if game["player"].colliderect(pu["rect"]):
            if pu["type"] == "life":
                game["lives"] += 1
            else:
                game["slow_timer"] = SLOW_DURATION
            game["powerups"].remove(pu)

        elif pu["rect"].top > HEIGHT:
            game["powerups"].remove(pu)

    if game["slow_timer"] > 0:
        game["slow_timer"] -= 1

    # ----- DRAW -----
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, game["player"])
    pygame.draw.ellipse(screen, BLACK, circle["rect"])

    for pu in game["powerups"]:
        color = GREEN if pu["type"] == "life" else YELLOW
        pygame.draw.rect(screen, color, pu["rect"])

    draw_text(f"Score: {game['score']}", font, BLACK, 10, 10)
    draw_text(f"Missed: {game['missed']}", font, BLACK, 10, 30)
    draw_text(f"Lives: {game['lives']}", font, BLACK, 10, 50)
    draw_text("P = Pause", font, BLACK, WIDTH - 90, 10)

    pygame.display.update()

pygame.quit()

# this is my commit  

