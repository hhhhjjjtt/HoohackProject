import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dinosaur variables
dino_x, dino_y = 100, 300
dino_speed = 5
dino_images = [pygame.image.load('images/character/c1.png'),
               pygame.image.load('images/character/c2.png')]
current_image = 0
animation_time = 10
current_time = 0

# Bullet variables
bullets = []  # List to store bullets
bullet_speed = 10

# Enemy variables
enemies = []
enemy_spawn_time = 5000  # 5 seconds in milliseconds
last_spawn_time = pygame.time.get_ticks()

# Base variables
base_health = 10
base_position = (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25)  # Center the base
base_size = (50, 50)  # Width and height of the base rectangle

# Shooting mode variables
shooting_mode = "pistol"  # Initial shooting mode


def shoot_bullet(mouse_pos, spread_angle=0):
    # Get character image size
    img_width, img_height = dino_images[current_image].get_size()

    # Calculate spawn position for the bullet (e.g., center-right of the character image)
    spawn_x = dino_x + img_width / 2
    spawn_y = dino_y + img_height / 2

    mouse_x, mouse_y = mouse_pos
    direction = pygame.math.Vector2(mouse_x - spawn_x, mouse_y - spawn_y).normalize()
    if spread_angle != 0:
        direction = direction.rotate(spread_angle)
    bullets.append([pygame.math.Vector2(spawn_x, spawn_y), direction])


def spawn_enemy():
    # Choose a random position outside the window
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, SCREEN_WIDTH)
        y = 0
    elif side == "bottom":
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT
    elif side == "left":
        x = 0
        y = random.randint(0, SCREEN_HEIGHT)
    else:  # right
        x = SCREEN_WIDTH
        y = random.randint(0, SCREEN_HEIGHT)

    speed = random.randint(3, 4)  # Random speed
    enemies.append(Enemy(x, y, speed))


def start_game(screen):
    global dino_x, dino_y, current_time, current_image, shooting_mode, last_spawn_time, base_health
    clock = pygame.time.Clock()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= enemy_spawn_time:
            spawn_enemy()
            last_spawn_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # shoot a bullet for mouseclick
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if shooting_mode == "pistol":
                        shoot_bullet(pygame.mouse.get_pos())
                    elif shooting_mode == "shotgun":
                        # Shoot 3 bullets with different angles
                        shoot_bullet(pygame.mouse.get_pos())
                        shoot_bullet(pygame.mouse.get_pos(), 10)  # Angle for spread
                        shoot_bullet(pygame.mouse.get_pos(), -10)
                if event.button == 3:
                    shooting_mode = "shotgun" if shooting_mode == "pistol" else "pistol"

        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dino_x -= dino_speed
        if keys[pygame.K_RIGHT]:
            dino_x += dino_speed
        if keys[pygame.K_UP]:
            dino_y -= dino_speed
        if keys[pygame.K_DOWN]:
            dino_y += dino_speed

        # Prevent going outside the window
        img_width, img_height = dino_images[current_image].get_size()
        dino_x = max(0, min(SCREEN_WIDTH - img_width, dino_x))
        dino_y = max(0, min(SCREEN_HEIGHT - img_height, dino_y))

        # Update dinosaur animation
        current_time += 1
        if current_time >= animation_time:
            current_time = 0
            current_image = (current_image + 1) % len(dino_images)

        # Update bullets
        for bullet in bullets:
            bullet[0] += bullet[1] * bullet_speed  # Update position

        # Clear Screen
        screen.fill(WHITE)

        # Draw Character
        screen.blit(dino_images[current_image], (dino_x, dino_y))

        # Draw Bullet
        for bullet in bullets:
            bullet_width = 0
            bullet_height = 0
            if shooting_mode == "pistol":
                bullet_width = 5
                bullet_height = 5
            if shooting_mode == "shotgun":
                bullet_width = 10
                bullet_height = 5
            pygame.draw.rect(screen, BLACK, (bullet[0].x - 5 // 2, bullet[0].y - 5 // 2, bullet_width, bullet_height))

        # Draw enemy
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        for enemy in enemies:
            enemy.move_towards_center(center_x, center_y)
            pygame.draw.rect(screen, BLACK, (enemy.x, enemy.y, 20, 20))  # Draw enemy as a black rectangle
            if math.hypot(center_x - enemy.x, center_y - enemy.y) < 25:  # Simple collision detection
                base_health -= 1  # Decrease base health
                enemies.remove(enemy)  # Remove the enemy that reached the base

        # Draw base
        pygame.draw.rect(screen, (178, 34, 34), pygame.Rect(base_position, base_size))

        # Display base's health
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"{base_health}/10", True, BLACK)
        screen.blit(health_text, (SCREEN_WIDTH - 150, 20))

        pygame.display.flip()
        clock.tick(30)


class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move_towards_center(self, center_x, center_y):
        direction = pygame.math.Vector2(center_x - self.x, center_y - self.y).normalize()
        self.x += direction.x * self.speed
        self.y += direction.y * self.speed
