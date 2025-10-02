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
SLIDER_TRACK_COLOR = (60, 60, 60)
SLIDER_HANDLE_COLOR = (100, 150, 200)

# -- Global Settings --
settings = {
    'brightness': 0.8  # 0.0 to 1.0
}

# -- Utility Functions --
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    surface.blit(text_surface, text_rect)

def draw_slider(surface, x, y, width, height, value, label):
    """Draw a slider with value 0.0 to 1.0"""
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]
    
    # Slider track
    track_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, SLIDER_TRACK_COLOR, track_rect)
    
    # Slider handle
    handle_x = x + (width - 20) * value
    handle_rect = pygame.Rect(handle_x, y - 5, 20, height + 10)
    pygame.draw.rect(surface, SLIDER_HANDLE_COLOR, handle_rect)
    
    # Check for interaction
    new_value = value
    if track_rect.collidepoint(mouse_pos) and mouse_click:
        relative_x = mouse_pos[0] - x
        new_value = max(0.0, min(1.0, relative_x / width))
    
    # Draw label and value
    font = pygame.font.Font(None, 24)
    label_text = font.render(f"{label}: {int(value * 100)}%", True, WHITE)
    surface.blit(label_text, (x, y - 30))
    
    return new_value

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

# -- Options Menu Loop --
def options_loop(screen, clock):
    global settings
    
    while True:
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"  # Back to main menu

        # Drawing
        screen.fill(BLACK)
        draw_text(screen, "OPTIONS", 64, WIDTH / 2, HEIGHT / 4)
        
        # Brightness slider
        settings['brightness'] = draw_slider(screen, WIDTH / 2 - 150, HEIGHT / 2, 300, 20, settings['brightness'], "Brightness")
        
        # Apply brightness overlay
        if settings['brightness'] < 1.0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(int((1.0 - settings['brightness']) * 255))
            screen.blit(overlay, (0, 0))
        
        # Back button
        back_button = draw_button(screen, "Back", WIDTH / 2 - 100, HEIGHT - 100, 200, 50)
        
        if back_button:
            return "MENU"
            
        pygame.display.flip()

# -- Main Menu Loop --
def menu_loop(screen, clock):
    selected_ship = 0  # 0=Blue, 1=Red
    ship_names = ['Blue', 'Red']
    
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
        options_button = draw_button(screen, "Options", WIDTH / 2 - 100, HEIGHT / 2 + 90, 200, 50)
        quit_button = draw_button(screen, "Quit", WIDTH / 2 - 100, HEIGHT / 2 + 150, 200, 50)
        
        # Controls info - diturunkan ke bawah agar tidak nabrak tombol Quit
        draw_text(screen, "Controls:", 24, WIDTH / 2, HEIGHT - 80)
        draw_text(screen, "WASD/Arrows: Move • Space: Shoot • P: Pause", 18, WIDTH / 2, HEIGHT - 55)

        if play_button:
            return ("PLAYING", selected_ship)
        if options_button:
            return "OPTIONS"
        if quit_button:
            return "QUIT"
            
        pygame.display.flip()

