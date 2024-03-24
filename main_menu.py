import pygame
import sys
import gameplay

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


def display_menu():
    font_path = "font/PublicPixel-z84yD.ttf"
    menu_font = pygame.font.Font(font_path, 20)  # Default font, size 40
    title_font = pygame.font.Font(font_path, 30)  # Larger font for the title

    background_image = pygame.image.load('images/menu.png')

    # Render the menu options
    start_text = menu_font.render('Press SPACE to Start', True, BLACK)
    quit_text = menu_font.render('Press Q to Quit', True, BLACK)
    title_text = title_font.render('DEFEND THE BISHOP', True, BLACK)

    # Create transparent surfaces for fade-in effect (menu options)
    start_surface = pygame.Surface(start_text.get_size(), pygame.SRCALPHA)
    quit_surface = pygame.Surface(quit_text.get_size(), pygame.SRCALPHA)
    title_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)  # Transparent surface for the title

    # Blit the text onto the transparent surfaces
    start_surface.blit(start_text, (0, 0))
    quit_surface.blit(quit_text, (0, 0))
    title_surface.blit(title_text, (0, 0))  # Blit the title text onto its surface

    alpha = 0  # Starting alpha
    increasing = True  # Control fade-in

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameplay.start_game(screen)  # Start the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(WHITE)

        screen.blit(background_image, (0, 0))

        # Update alpha for fade-in effect
        if increasing:
            alpha += 4
            if alpha >= 255:
                alpha = 255
                increasing = False  # Optionally reset to keep looping

        # Set the alpha value for the surfaces
        start_surface.set_alpha(alpha)
        quit_surface.set_alpha(alpha)
        title_surface.set_alpha(alpha)  # Apply the alpha to the title surface as well

        # Calculate positions
        start_rect = start_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        quit_rect = quit_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))  # Position the title at the top

        # Blit the surfaces with the text to the screen
        screen.blit(title_surface, title_rect)  # Draw the title
        screen.blit(start_surface, start_rect)
        screen.blit(quit_surface, quit_rect)

        pygame.display.flip()
        pygame.time.delay(100)  # Control fade speed


if __name__ == '__main__':
    display_menu()