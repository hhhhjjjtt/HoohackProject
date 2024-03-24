import pygame
import sys
import math
import random

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and play background music
pygame.mixer.music.load('audios/BGM.mp3')
pygame.mixer.music.play(-1)

# Game state
game_state = "playing"  # Can be "playing" or "game_over"

# Dinosaur variables
dino_x, dino_y = 100, 300
dino_speed = 5
stand_images = [pygame.image.load('images/character/c1.png'),
               pygame.image.load('images/character/c2.png')]
walk_images = [pygame.image.load('images/character/w1.png'),
               pygame.image.load('images/character/w2.png')]
current_images = stand_images
current_image = 0
animation_time = 10
current_time = 0
kill_count = 0  # kill count
facing_right = True
is_moving = False  # Track whether the character is moving

# Time variables
last_frame_change_time = pygame.time.get_ticks()
frame_change_interval = 250  # Change frame every __ milliseconds

# Bullet variables
bullets = []  # List to store bullets
bullet_speed = 15

# Enemy variables
enemies = []
enemy_spawn_time = 5000  # 5 seconds in milliseconds
enemy_spawn_count = 0
last_spawn_time = pygame.time.get_ticks()
enemy_image = pygame.image.load('images/enemy/pawn.png')

# Base variables
base_health = 10
base_position = (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25)  # Center the base
base_size = (50, 50)  # Width and height of the base rectangle

# Shooting mode variables
shooting_mode = "pistol"  # Initial shooting mode

# Range limit
SHOTGUN_RANGE = 200
PISTOL_RANGE = 350

font_path = "font/PublicPixel-z84yD.ttf"

def shoot_bullet(mouse_pos, spread_angle=0, is_shotgun=False):
    # Get character image size
    img_width, img_height = stand_images[current_image].get_size()

    # Calculate spawn position for the bullet
    spawn_x = dino_x + img_width / 2
    spawn_y = dino_y + img_height / 2

    mouse_x, mouse_y = mouse_pos
    direction = pygame.math.Vector2(mouse_x - spawn_x, mouse_y - spawn_y).normalize()
    if spread_angle != 0:
        direction = direction.rotate(spread_angle)
    bullets.append([pygame.math.Vector2(spawn_x, spawn_y), direction, 0, is_shotgun])


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
    global dino_x, dino_y, current_time, current_image, shooting_mode, last_spawn_time, base_health, game_state, \
        enemy_spawn_time, enemy_spawn_count, kill_count, last_frame_change_time, current_images, facing_right, font_path
    clock = pygame.time.Clock()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game
                        game_state = "playing"
                        base_health = 10
                        enemies.clear()
                        bullets.clear()
                        dino_x, dino_y = 100, 300
                        enemy_spawn_count = 0
                        kill_count = 0
            if game_state == "playing":
                # shoot a bullet for mouseclick
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if shooting_mode == "pistol":
                            shoot_bullet(pygame.mouse.get_pos())
                        elif shooting_mode == "shotgun":
                            # Shoot 3 bullets with different angles
                            shoot_bullet(pygame.mouse.get_pos(), 0, True)
                            shoot_bullet(pygame.mouse.get_pos(), 10, True)  # Angle for spread
                            shoot_bullet(pygame.mouse.get_pos(), -10, True)
                    if event.button == 3:
                        shooting_mode = "shotgun" if shooting_mode == "pistol" else "pistol"

        if game_state == "playing":
            # Spawn enemy
            if current_time - last_spawn_time >= enemy_spawn_time:
                spawn_enemy()
                enemy_spawn_count += 1
                if enemy_spawn_count > 2:
                    enemy_spawn_time = 4500
                if enemy_spawn_count > 4:
                    enemy_spawn_time = 4000
                if enemy_spawn_count > 6:
                    enemy_spawn_time = 3500
                if enemy_spawn_count > 8:
                    enemy_spawn_time = 3000
                if enemy_spawn_count > 10:
                    enemy_spawn_time = 2000
                if enemy_spawn_count > 15:
                    spawn_enemy()
                last_spawn_time = current_time

            # Movement controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                dino_x -= dino_speed
                facing_right = False
            if keys[pygame.K_RIGHT]:
                dino_x += dino_speed
                facing_right = True
            if keys[pygame.K_UP]:
                dino_y -= dino_speed
            if keys[pygame.K_DOWN]:
                dino_y += dino_speed

            # Decide if we need to flip the image
            current_frame = current_images[current_image]
            if not facing_right:
                current_frame = pygame.transform.flip(current_frame, True, False)

            # Prevent going outside the window
            img_width, img_height = stand_images[current_image].get_size()
            dino_x = max(0, min(SCREEN_WIDTH - img_width, dino_x))
            dino_y = max(0, min(SCREEN_HEIGHT - img_height, dino_y))

            is_moving = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]
            if is_moving:
                current_images = walk_images
            else:
                current_images = stand_images

            if current_time - last_frame_change_time >= frame_change_interval:
                current_image = (current_image + 1) % len(current_images)
                last_frame_change_time = current_time


            if base_health <= 0:
                game_state = "game_over"

            # Clear Screen
            screen.fill(WHITE)

            # Draw Character
            screen.blit(current_frame, (dino_x, dino_y))

            # Draw Bullet
            for bullet in bullets[:]:
                bullet[0] += bullet[1] * bullet_speed  # Update bullet position
                bullet[2] += bullet_speed

                bullet_width, bullet_height = (10, 5) if bullet[3] else (5, 5)

                # check to remove the bullet reaching range
                if bullet[3] and bullet[2] > SHOTGUN_RANGE:  # bullet[3] is is_shotgun flag
                    bullets.remove(bullet)
                    continue

                if bullet[2] > PISTOL_RANGE:
                    bullets.remove(bullet)
                    continue

                bullet_hit = False
                for enemy in enemies[:]:
                    if enemy.is_collided_with_bullet(bullet):
                        enemy.health -= 5
                        bullets.remove(bullet)
                        bullet_hit = True
                        break  # Stop checking for other collisions
                if bullet_hit:
                    continue  # Skip drawing this bullet
                pygame.draw.rect(screen, BLACK, (bullet[0].x - 5 // 2, bullet[0].y - 5 // 2, bullet_width, bullet_height))

            # Draw enemy
            center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            for enemy in enemies:
                enemy.move_towards_center(center_x, center_y)
                enemy.draw(screen)
                enemy.draw_health_bar(screen)  # Draw enemy health bar
                if enemy.health <= 0:
                    kill_count += 1
                    enemies.remove(enemy)  # Remove enemy if health is 0 or less
                if math.hypot(center_x - enemy.x, center_y - enemy.y) < 25:  # Simple collision detection
                    base_health -= 1  # Decrease base health
                    enemies.remove(enemy)  # Remove the enemy that reached the base

            # Draw base
            base_image = pygame.image.load('images/base/bishop.png')
            screen.blit(base_image, base_position)

            # Display base's health
            font = pygame.font.Font(font_path, 15)
            health_text = font.render(f"{base_health}/10", True, BLACK)
            screen.blit(health_text, (SCREEN_WIDTH - 150, 20))

            # Display kill count
            font = pygame.font.Font(font_path, 15)
            kill_text = font.render(f"Kill Count: {kill_count}", True, BLACK)
            screen.blit(kill_text, (50, 20))

        elif game_state == "game_over":
            # Display game over message and restart option
            screen.fill(WHITE)  # Optional: Choose whether to clear screen or keep the last frame visible
            font_big = pygame.font.Font(font_path, 74)
            font_small = pygame.font.Font(font_path, 36)
            game_over_text = font_big.render("Game Over", True, BLACK)
            restart_text = font_small.render("Press R to Restart", True, BLACK)
            screen.blit(game_over_text, (
            SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

        pygame.display.flip()
        clock.tick(30)


class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = 10  # Each enemy starts with 10 health points
        self.image = enemy_image

    def move_towards_center(self, center_x, center_y):
        direction = pygame.math.Vector2(center_x - self.x, center_y - self.y).normalize()
        self.x += direction.x * self.speed
        self.y += direction.y * self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # Draw enemy image
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        # Draw a red health bar above the enemy
        health_bar_width = 24
        health_bar_height = 5
        fill_width = (self.health / 10) * health_bar_width
        pygame.draw.rect(screen, (178, 34, 34), (self.x, self.y + 26, fill_width, health_bar_height))

    def is_collided_with_bullet(self, bullet):
        # Simple collision detection between enemy and bullet
        enemy_rect = pygame.Rect(self.x, self.y, 20, 20)  # Assuming enemy is drawn as a 20x20 rectangle
        bullet_rect = pygame.Rect(bullet[0].x, bullet[0].y, 5, 5)  # Assuming bullet is drawn as a 5x5 rectangle
        return enemy_rect.colliderect(bullet_rect)
