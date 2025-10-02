import pygame
import sys
import os

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

# -- Ship Animation Class --
class ShipDisplay:
    def __init__(self, ship_animations):
        self.ship_animations = ship_animations  # List of animation frames per ship
        self.animation_offset = 0
        self.animation_speed = 0.08
        self.animation_direction = 1
        self.max_offset = 15
        
        # Frame animation
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 10  # Frames per second untuk animasi
        
    def update(self):
        # Update animasi gerak kanan-kiri
        self.animation_offset += self.animation_speed * self.animation_direction
        if self.animation_offset >= self.max_offset or self.animation_offset <= -self.max_offset:
            self.animation_direction *= -1
            
        # Update frame animasi
        self.frame_timer += 1
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            if len(self.ship_animations) > 0 and len(self.ship_animations[0]) > 0:
                self.frame_index = (self.frame_index + 1) % len(self.ship_animations[0])
    
    def draw(self, surface, ship_type, x, y):
        # Gambar ship dengan offset animasi dan frame animasi
        if ship_type < len(self.ship_animations) and len(self.ship_animations[ship_type]) > 0:
            ship_img = self.ship_animations[ship_type][self.frame_index]
            ship_rect = ship_img.get_rect(center=(x + self.animation_offset, y))
            surface.blit(ship_img, ship_rect)

# -- Utility Functions --
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
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
    # Load ship animations (frame 1, 2, 3)
    assets_folder = "Assets"
    game_assets_folder = os.path.join(assets_folder, "PixelSpaceRage", "256px")
    
    ship_animations = []
    ship_names = ['Blue', 'Red']
    ship_prefixes = ['PlayerBlue_Frame_', 'PlayerRed_Frame_']
    
    # Load ship animation frames
    for prefix in ship_prefixes:
        frames = []
        for frame_num in ['01', '02', '03']:
            try:
                img_path = os.path.join(game_assets_folder, f"{prefix}{frame_num}_png_processed.png")
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (80, 80))  # Scale untuk display
                frames.append(img)
            except:
                # Fallback jika gambar tidak ditemukan
                fallback_surface = pygame.Surface((80, 80))
                fallback_surface.fill((100, 100, 100))
                frames.append(fallback_surface)
        ship_animations.append(frames)
    
    selected_ship = 0
    ship_display = ShipDisplay(ship_animations)
    
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

        # Update animasi
        ship_display.update()

        # Drawing
        screen.fill(BLACK)
        draw_text(screen, "SPACE SHOOTER", 64, WIDTH / 2, HEIGHT / 6)
        
        # Ship selection display
        draw_text(screen, "Select Ship:", 30, WIDTH / 2, HEIGHT / 2 - 120)
        
        # Draw ship image dengan animasi (tanpa tulisan < Blue > atau < Red >)
        ship_display.draw(screen, selected_ship, WIDTH / 2, HEIGHT / 2 - 50)
        
        # Draw ship description
        descriptions = [
            "Balanced fighter with standard speed",
            "Fast fighter with increased speed"
        ]
        draw_text(screen, descriptions[selected_ship], 24, WIDTH / 2, HEIGHT / 2 + 10)
        
        # Draw instruction
        draw_text(screen, "Use ← → arrows to change ship", 20, WIDTH / 2, HEIGHT / 2 + 40)
        
        # Buttons
        play_button = draw_button(screen, "Play", WIDTH / 2 - 100, HEIGHT / 2 + 80, 200, 50)
        options_button = draw_button(screen, "Options", WIDTH / 2 - 100, HEIGHT / 2 + 140, 200, 50)
        quit_button = draw_button(screen, "Quit", WIDTH / 2 - 100, HEIGHT / 2 + 200, 200, 50)
        
        # Controls info
        draw_text(screen, "Controls:", 20, WIDTH / 2, HEIGHT - 30)
        draw_text(screen, "WASD/Arrows: Move • Space: Shoot • P: Pause", 16, WIDTH / 2, HEIGHT - 15)

        if play_button:
            return ("PLAYING", selected_ship)
        if options_button:
            return "OPTIONS"
        if quit_button:
            return "QUIT"
            
        pygame.display.flip()

