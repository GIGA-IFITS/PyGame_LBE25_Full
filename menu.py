import pygame
import sys

# -- Constants --
HEIGHT = 600
WIDTH = 800

# -- Colours --
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_INACTIVE_COLOR = (20, 50, 100)
BUTTON_ACTIVE_COLOR = (40, 80, 150)

# -- Utility Functions --
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    surface.blit(text_surface, text_rect)

def draw_button(surface, text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    
    rect = pygame.Rect(x, y, width, height)
    on_button = rect.collidepoint(mouse_pos)

    if on_button:
        pygame.draw.rect(surface, BUTTON_ACTIVE_COLOR, rect)
        if click:
            return True
    else:
        pygame.draw.rect(surface, BUTTON_INACTIVE_COLOR, rect)

    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
    return False

# -- Main Menu Loop --
def menu_loop(screen, clock):
    while True:
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"

        # Drawing
        screen.fill(BLACK)
        draw_text(screen, "SPACE SHOOTER", 64, WIDTH / 2, HEIGHT / 4)
        
        play_button = draw_button(screen, "Play", WIDTH / 2 - 100, HEIGHT / 2, 200, 50)
        quit_button = draw_button(screen, "Quit", WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50)

        if play_button:
            return "PLAYING"
        if quit_button:
            return "QUIT"
            
        pygame.display.flip()

