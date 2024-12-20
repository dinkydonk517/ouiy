import pygame
import random
import math
import time

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_alive = True
survival_time = 0
start_time = time.time()

triangles = []
triangle_lifetime = 8

def spawn_triangle(current_time):
    """Spawn a new triangle with a random direction."""
    angle = random.uniform(0, 90)
    new_direction = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle)))
    new_position = pygame.Vector2(30, 30)
    triangles.append((new_position.copy(), new_direction, current_time))

while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        current_time = time.time()
        triangles = [t for t in triangles if current_time - t[2] < triangle_lifetime]

        for position, direction, spawn_time in triangles:
            pygame.draw.polygon(screen, "red", [position, position + pygame.Vector2(20, 30), position + pygame.Vector2(40, 30)])
            position += direction * 300 * dt  

            if player_alive and position.distance_to(player_pos) < 20:
                player_alive = False
                survival_time = round(current_time - start_time, 2)
                print(f"Game Over. You survived for {survival_time} seconds.")

        if random.random() < 0.30:
            spawn_triangle(current_time)

        if player_alive:
            pygame.draw.circle(screen, "red", (int(player_pos.x), int(player_pos.y)), 20)

        keys = pygame.key.get_pressed()
        if player_alive:
            if keys[pygame.K_w]:
                player_pos.y -= 300 * dt
            if keys[pygame.K_s]:
                player_pos.y += 300 * dt
            if keys[pygame.K_a]:
                player_pos.x -= 300 * dt
            if keys[pygame.K_d]:
                player_pos.x += 300 * dt
            if keys[pygame.K_e]:
                player_pos.x += 500 * dt

        if not player_alive:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, "white")
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
            time_text = font.render(f"You survived for {survival_time} seconds", True, "white")
            screen.blit(time_text, (screen.get_width() // 2 - time_text.get_width() // 2, screen.get_height() // 2 + 50))

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    except Exception as e:
        print(f"An error occurred: {e}")

pygame.quit()
