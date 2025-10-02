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
    selected_ship = 0  # 0=Blue, 1=Red, 2=Shadow
    ship_names = ['Blue', 'Red', 'Shadow']
    
    while True:
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"
                # Ship selection with arrow keys
                if event.key == pygame.K_LEFT:
                    selected_ship = (selected_ship - 1) % len(ship_names)
                elif event.key == pygame.K_RIGHT:
                    selected_ship = (selected_ship + 1) % len(ship_names)

        # Drawing
        screen.fill(BLACK)
        draw_text(screen, "SPACE SHOOTER", 64, WIDTH / 2, HEIGHT / 4)
        
        # Ship selection display
        draw_text(screen, "Select Ship:", 30, WIDTH / 2, HEIGHT / 2 - 80)
        draw_text(screen, f"< {ship_names[selected_ship]} >", 36, WIDTH / 2, HEIGHT / 2 - 40, (100, 200, 255))
        draw_text(screen, "Use ← → arrows to change ship", 20, WIDTH / 2, HEIGHT / 2 - 10)
        
        play_button = draw_button(screen, "Play", WIDTH / 2 - 100, HEIGHT / 2 + 30, 200, 50)
        quit_button = draw_button(screen, "Quit", WIDTH / 2 - 100, HEIGHT / 2 + 100, 200, 50)
        
        # Controls info
        draw_text(screen, "Controls:", 24, WIDTH / 2, HEIGHT - 120)
        draw_text(screen, "WASD/Arrows: Move • Space: Shoot • C: Change Ship • P: Pause", 18, WIDTH / 2, HEIGHT - 95)

        if play_button:
            return ("PLAYING", selected_ship)
        if quit_button:
            return "QUIT"
            
        pygame.display.flip()

