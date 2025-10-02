import pygame
import random
import os
import sys

# -- Constants --
HEIGHT = 600
WIDTH = 800
PLAYER_HEIGHT = 50
PLAYER_WIDTH = 50

# -- Colours --
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# -- Utility Function --
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# -- Classes --
class Player(pygame.sprite.Sprite):
    def __init__(self, game_assets_folder):
        super().__init__()
        player_img_path = os.path.join(game_assets_folder, "PlayerBlue_Frame_01_png_processed.png")
        self.original_image = pygame.image.load(player_img_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect(centerx=WIDTH / 2, bottom=HEIGHT - 10)
        self.radius = 20
        
    def update(self):
        keys = pygame.key.get_pressed()
        speed = 5
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0: self.rect.x -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH: self.rect.x += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0: self.rect.y -= speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT: self.rect.y += speed

class Block(pygame.sprite.Sprite):
    def __init__(self, image_list):
        super().__init__()
        self.original_image = random.choice(image_list)
        self.image = self.original_image
        self.rect = self.image.get_rect(x=random.randrange(WIDTH - self.image.get_width()), y=random.randrange(-100, -40))
        self.radius = int(self.rect.width * 0.85 / 2)
        self.speed_y = random.randrange(2, 6)
        self.speed_x = random.randrange(-2, 2)
        self.rotation = 0
        self.rotation_speed = random.randint(-5, 5)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.original_image, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect(center=old_center)

    def update(self):
        self.rotate()
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, explosion_anim):
        super().__init__()
        self.explosion_anim = explosion_anim
        self.image = self.explosion_anim[0]
        self.rect = self.image.get_rect(center=center)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect(center=center)

# -- Main Game Loop --
def game_loop(screen, clock, assets):
    # Setup
    game_assets_folder = os.path.join("Assets", "PixelSpaceRage", "256px")
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player(game_assets_folder)
    all_sprites.add(player)
    
    def spawn_new_block():
        block = Block(assets['meteor_images'])
        all_sprites.add(block)
        enemies.add(block)

    for _ in range(8):
        spawn_new_block()

    score = 0
    game_sub_state = "PLAYING" # "PLAYING", "PAUSED", "GAME_OVER"

    pygame.mixer.music.load(assets['background_music'])
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    running = True
    while running:
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return "QUIT"
                if game_sub_state == "PLAYING" and event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top, assets['bullet_img'])
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if game_sub_state == "GAME_OVER" and event.key == pygame.K_r:
                    return "PLAYING" # Kembali ke main.py untuk restart
                if game_sub_state == "GAME_OVER" and event.key == pygame.K_x:
                    return "MENU" # Kembali ke menu
                if game_sub_state == "PLAYING" and event.key == pygame.K_p:
                    game_sub_state = "PAUSED"
                    pygame.mixer.music.pause()
                elif game_sub_state == "PAUSED" and event.key == pygame.K_p:
                    game_sub_state = "PLAYING"
                    pygame.mixer.music.unpause()

        # Update
        if game_sub_state == "PLAYING":
            all_sprites.update()
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 50
                expl = Explosion(hit.rect.center, assets['explosion_anim'])
                all_sprites.add(expl)
                spawn_new_block()
            
            hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
            if hits:
                player_expl = Explosion(player.rect.center, assets['explosion_anim'])
                all_sprites.add(player_expl)
                player.kill()
                pygame.mixer.music.stop()

            if not player.alive():
                game_sub_state = "GAME_OVER"

        elif game_sub_state == "GAME_OVER":
            all_sprites.update() # Hanya update ledakan dll

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 30, WIDTH / 2, 10)
        
        if game_sub_state == "PAUSED":
            draw_text(screen, "Game Paused", 48, WIDTH / 2, HEIGHT / 2 - 50)
            draw_text(screen, "Press P to Continue", 22, WIDTH / 2, HEIGHT / 2)
        elif game_sub_state == "GAME_OVER":
            draw_text(screen, "GAME OVER!", 64, WIDTH / 2, HEIGHT / 4)
            draw_text(screen, "Press R to restart the game", 30, WIDTH / 2, HEIGHT / 2)
            draw_text(screen, "Press X to exit to main menu", 22, WIDTH / 2, HEIGHT / 2 + 50)

        pygame.display.flip()
