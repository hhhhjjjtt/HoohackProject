import pygame
import sys
import gameplay

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def display_menu():
    menu_font = pygame.font.Font(None, 40)  # Default font, size 40
    start_text = menu_font.render('Press SPACE to Start', True, BLACK)
    quit_text = menu_font.render('Press Q to Quit', True, BLACK)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    screen.fill(WHITE)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameplay.start_game(screen)  # Start the game
                    waiting_for_input = False  # Exit menu after the game is over to show the menu again
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    display_menu()
