import json
import os
import pygame

# High Score Management
class HighScoreManager:
    def __init__(self):
        self.highscore_file = "highscores.json"
        self.highscores = self.load_highscores()
    
    def load_highscores(self):
        """Load high scores from file"""
        try:
            with open(self.highscore_file, 'r') as file:
                scores = json.load(file)
                # Sort by score descending
                return sorted(scores, key=lambda x: x['score'], reverse=True)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Return empty list if file doesn't exist or is invalid
            return []
    
    def save_highscores(self):
        """Save high scores to file"""
        try:
            with open(self.highscore_file, 'w') as file:
                json.dump(self.highscores, file, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def add_score(self, name, score):
        """Add a new score to the high scores"""
        self.highscores.append({'name': name, 'score': score})
        # Sort by score descending and keep only top 10
        self.highscores = sorted(self.highscores, key=lambda x: x['score'], reverse=True)[:10]
        self.save_highscores()
    
    def get_top_scores(self, count=10):
        """Get top N scores"""
        return self.highscores[:count]
    
    def is_high_score(self, score):
        """Check if score qualifies as a high score (top 10)"""
        if len(self.highscores) < 10:
            return True
        return score > self.highscores[9]['score']

def draw_text_centered(screen, text, size, x, y, color=(255, 255, 255)):
    """Draw text centered at given position"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def input_name_screen(screen, clock, score):
    """Screen for inputting player name after achieving high score"""
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    
    name = ""
    input_active = True
    cursor_visible = True
    cursor_timer = 0
    
    while input_active:
        clock.tick(60)
        cursor_timer += 1
        
        # Toggle cursor visibility every 30 frames (0.5 seconds)
        if cursor_timer >= 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip():  # Only accept non-empty names
                        return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None
                else:
                    # Add character to name (max 15 characters)
                    if len(name) < 15 and event.unicode.isprintable():
                        name += event.unicode
        
        # Draw
        screen.fill((0, 0, 0))
        
        # Title
        draw_text_centered(screen, "NEW HIGH SCORE!", 48, WIDTH//2, HEIGHT//2 - 100, (255, 255, 0))
        draw_text_centered(screen, f"Score: {score}", 36, WIDTH//2, HEIGHT//2 - 60, (255, 255, 255))
        
        # Name input
        draw_text_centered(screen, "Enter your name:", 32, WIDTH//2, HEIGHT//2 - 20, (255, 255, 255))
        
        # Input box
        input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 40)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        
        # Name text with cursor
        display_name = name
        if cursor_visible:
            display_name += "|"
        
        font = pygame.font.Font(None, 36)
        name_surface = font.render(display_name, True, (255, 255, 255))
        screen.blit(name_surface, (input_box.x + 5, input_box.y + 5))
        
        # Instructions
        draw_text_centered(screen, "Press ENTER to save, ESC to skip", 24, WIDTH//2, HEIGHT//2 + 80, (200, 200, 200))
        
        pygame.display.flip()
    
    return None

def show_highscores(screen, clock, highscore_manager):
    """Display high scores screen"""
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    
    scores = highscore_manager.get_top_scores(10)
    
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return "MENU"
        
        # Draw
        screen.fill((0, 0, 0))
        
        # Title
        draw_text_centered(screen, "HIGH SCORES", 48, WIDTH//2, 80, (255, 255, 0))
        
        # Scores
        if scores:
            for i, score_data in enumerate(scores):
                y_pos = 150 + i * 35
                rank = f"{i+1:2d}."
                name = score_data['name'][:12]  # Limit name display length
                score = f"{score_data['score']:,}"
                
                # Rank
                font = pygame.font.Font(None, 32)
                rank_surface = font.render(rank, True, (255, 255, 255))
                screen.blit(rank_surface, (WIDTH//2 - 200, y_pos))
                
                # Name
                name_surface = font.render(name, True, (255, 255, 255))
                screen.blit(name_surface, (WIDTH//2 - 150, y_pos))
                
                # Score
                score_surface = font.render(score, True, (255, 255, 255))
                score_rect = score_surface.get_rect()
                screen.blit(score_surface, (WIDTH//2 + 150 - score_rect.width, y_pos))
        else:
            draw_text_centered(screen, "No high scores yet!", 36, WIDTH//2, HEIGHT//2, (200, 200, 200))
        
        # Instructions
        draw_text_centered(screen, "Press ESC or ENTER to return to menu", 24, WIDTH//2, HEIGHT - 50, (200, 200, 200))
        
        pygame.display.flip()