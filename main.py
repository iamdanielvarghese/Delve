# main.py
import pygame
import random
import time  # NEW: Needed for the stopwatch
import numpy as np
from noise_level import generate_terrain, MAP_W, MAP_H
from database_manager import DatabaseManager

TILE = 12

# Constants
TYPE_FLOOR = 0
TYPE_WALL = 1

# --- COLORS ---
COLOR_WALL = (30, 30, 35)
COLOR_FLOOR = (100, 90, 80)
COLOR_PLAYER = (255, 215, 0)
COLOR_EXIT = (0, 255, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_UI_BG = (0, 0, 0, 150)  # Semi-transparent black for UI

PALETTE = [COLOR_FLOOR, COLOR_WALL]


def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))


def draw_map(screen, biomes):
    for y in range(MAP_H):
        for x in range(MAP_W):
            tile_type = biomes[y, x]
            base_color = PALETTE[tile_type]

            variance = random.randint(-10, 10)
            r = clamp(base_color[0] + variance, 0, 255)
            g = clamp(base_color[1] + variance, 0, 255)
            b = clamp(base_color[2] + variance, 0, 255)

            pygame.draw.rect(screen, (r, g, b),
                             (x * TILE, y * TILE, TILE, TILE))


def place_objects(biomes):
    # 1. Place Player
    while True:
        px = random.randint(1, MAP_W - 2)
        py = random.randint(1, MAP_H - 2)
        if biomes[py, px] == TYPE_FLOOR:
            player_pos = (px, py)
            break

    # 2. Place Exit (Must be far away)
    attempt = 0
    while True:
        ex = random.randint(1, MAP_W - 2)
        ey = random.randint(1, MAP_H - 2)
        dist = abs(ex - player_pos[0]) + abs(ey - player_pos[1])

        if biomes[ey, ex] == TYPE_FLOOR:
            if dist > 40 or attempt > 1000:
                exit_pos = (ex, ey)
                break
        attempt += 1

    return player_pos, exit_pos


def draw_leaderboard(screen, db):
    """Fetches and draws the top 5 scores."""
    scores = db.get_top_scores()

    # Draw semi-transparent background box
    s = pygame.Surface((400, 300))
    s.set_alpha(220)
    s.fill((0, 0, 0))
    rect = s.get_rect(center=(MAP_W * TILE // 2, MAP_H * TILE // 2))
    screen.blit(s, rect)

    font_title = pygame.font.SysFont(None, 40)
    font_text = pygame.font.SysFont(None, 28)

    # Title
    title = font_title.render("TOP SPEEDS (Global)", True, (255, 215, 0))
    screen.blit(title, (rect.x + 80, rect.y + 20))

    # List scores
    y_offset = 70
    if not scores:
        txt = font_text.render("No records yet!", True, (200, 200, 200))
        screen.blit(txt, (rect.x + 120, rect.y + y_offset))
    else:
        for idx, (lvl, time_val, date) in enumerate(scores):
            # Format: 1. Level 5 - 12.34s
            row_str = f"{idx+1}. Level {lvl}  -  {time_val:.2f}s"
            txt = font_text.render(row_str, True, (255, 255, 255))
            screen.blit(txt, (rect.x + 50, rect.y + y_offset))
            y_offset += 35

    pygame.display.flip()

    # Wait for key press to close
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting = False


def main():
    pygame.init()
    screen = pygame.display.set_mode((MAP_W * TILE, MAP_H * TILE))
    pygame.display.set_caption(
        "Delve - Press 'L' for Leaderboard - Press Arrow Keys for Movement")
    clock = pygame.time.Clock()
    font_ui = pygame.font.SysFont(None, 32)

    db = DatabaseManager()

    current_level = 1

    # --- INITIAL SETUP ---
    biomes, used_seed = generate_terrain(seed=None)
    (px, py), (ex, ey) = place_objects(biomes)

    map_surface = pygame.Surface((MAP_W * TILE, MAP_H * TILE))
    draw_map(map_surface, biomes)

    # STOPWATCH START
    start_time = time.time()

    running = True
    while running:
        clock.tick(60)

        # Calculate elapsed time
        current_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                new_x, new_y = px, py

                if event.key == pygame.K_LEFT:
                    new_x -= 1
                elif event.key == pygame.K_RIGHT:
                    new_x += 1
                elif event.key == pygame.K_UP:
                    new_y -= 1
                elif event.key == pygame.K_DOWN:
                    new_y += 1

                # Show Leaderboard
                elif event.key == pygame.K_l:
                    draw_leaderboard(screen, db)
                    # Reset clock logic so time doesn't tick while in menu
                    # (Simple hack: just reset the start_time offset)
                    start_time = time.time() - current_time

                # Move Player
                if 0 <= new_x < MAP_W and 0 <= new_y < MAP_H:
                    if biomes[new_y, new_x] == TYPE_FLOOR:
                        px, py = new_x, new_y

        # --- WIN CONDITION ---
        if px == ex and py == ey:
            # 1. Capture Final Time
            final_time = current_time

            # 2. Save to DB
            db.save_score(current_level, used_seed, final_time)

            # 3. Show "Level Complete" Message
            msg = font_ui.render(
                f"Level {current_level} Done! Time: {final_time:.2f}s", True, COLOR_PLAYER)
            msg_bg = msg.get_rect(center=(MAP_W*TILE//2, MAP_H*TILE//2))
            pygame.draw.rect(screen, (0, 0, 0), msg_bg.inflate(20, 20))
            screen.blit(msg, msg_bg)
            pygame.display.flip()
            pygame.time.delay(1500)

            # 4. Next Level Setup
            current_level += 1
            biomes, used_seed = generate_terrain(seed=None)
            draw_map(map_surface, biomes)
            (px, py), (ex, ey) = place_objects(biomes)

            # 5. Reset Timer
            start_time = time.time()
            continue

        # --- DRAWING ---
        screen.blit(map_surface, (0, 0))

        # Draw Objects
        pygame.draw.rect(screen, COLOR_EXIT,
                         (ex * TILE, ey * TILE, TILE, TILE))
        pygame.draw.rect(screen, COLOR_PLAYER,
                         (px * TILE, py * TILE, TILE, TILE))

        # Draw UI (Timer)
        timer_text = f"Level {current_level}  |  Time: {current_time:.2f}"
        img_ui = font_ui.render(timer_text, True, COLOR_TEXT)
        pygame.draw.rect(screen, (0, 0, 0), (5, 5, 250, 30)
                         )  # Black box background
        screen.blit(img_ui, (15, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
