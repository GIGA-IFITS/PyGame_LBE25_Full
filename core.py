import pygame
import random
import os
import sys
from highscore import HighScoreManager, input_name_screen

# -- Constants --
HEIGHT = 700
WIDTH = 1000
PLAYER_HEIGHT = 70
PLAYER_WIDTH = 70

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
        self.game_assets_folder = game_assets_folder
        
        # Define available ship types
        self.ship_types = ['Blue', 'Red']
        self.current_ship_index = 0
        
        # Animation properties
        self.animation_frames = []
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 10
        self.facing_right = True
        self.is_moving = False
        
        # Shooting cooldown
        self.last_shot = 0
        self.shoot_cooldown = 250  # 0.25 seconds in milliseconds
        
        # Health system
        self.health = 1
        self.max_health = 3
        
        # Powerup effects
        self.ammo_boost_end = 0
        self.rocket_boost_end = 0
        self.shield_end = 0
        self.is_shielded = False
        
        # Load ship animations
        self.load_ship_animations()
        self.rect = self.image.get_rect(centerx=WIDTH / 2, bottom=HEIGHT - 10)
        self.radius = 20
    
    def load_ship_animations(self):
        """Load animation frames for current ship"""
        current_ship = self.ship_types[self.current_ship_index]
        ship_prefix = f"Player{current_ship}_Frame_"
        
        self.animation_frames = []
        for frame_num in ['01', '02', '03']:
            try:
                img_path = os.path.join(self.game_assets_folder, f"{ship_prefix}{frame_num}_png_processed.png")
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.animation_frames.append(img)
            except:
                # Fallback to first frame if others don't exist
                if len(self.animation_frames) > 0:
                    self.animation_frames.append(self.animation_frames[0])
        
        if len(self.animation_frames) > 0:
            self.image = self.animation_frames[0]
        else:
            # Ultimate fallback
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill((100, 100, 100))
    
    def change_ship(self):
        """Change to the next ship type"""
        self.current_ship_index = (self.current_ship_index + 1) % len(self.ship_types)
        old_center = self.rect.center
        self.load_ship_animations()
        self.rect = self.image.get_rect(center=old_center)
    
    def get_current_ship_name(self):
        """Get the name of the current ship"""
        return self.ship_types[self.current_ship_index]
    
    def get_ship_stats(self):
        """Get special stats for different ships"""
        stats = {
            'Blue': {'speed_bonus': 0, 'description': 'Balanced'},
            'Red': {'speed_bonus': 1, 'description': 'Fast'}
        }
        return stats[self.get_current_ship_name()]
    
    def can_shoot(self):
        """Check if player can shoot based on cooldown or ammo boost"""
        now = pygame.time.get_ticks()
        if now < self.ammo_boost_end:  # Ammo boost active
            return True
        return now - self.last_shot >= self.shoot_cooldown
    
    def shoot(self):
        """Record that player has shot"""
        if pygame.time.get_ticks() >= self.ammo_boost_end:  # Only record if not boosted
            self.last_shot = pygame.time.get_ticks()
    
    def take_damage(self):
        """Take damage if not shielded"""
        if not self.is_shielded:
            self.health -= 1
            return self.health <= 0  # Return True if dead
        return False
    
    def heal(self):
        """Heal player"""
        self.health = min(self.health + 1, self.max_health)
    
    def activate_ammo_boost(self):
        """Activate ammo boost for 10 seconds"""
        self.ammo_boost_end = pygame.time.get_ticks() + 10000
    
    def activate_rocket_boost(self):
        """Activate rocket boost for 10 seconds"""
        self.rocket_boost_end = pygame.time.get_ticks() + 10000
    
    def activate_shield(self):
        """Activate shield for 10 seconds"""
        self.shield_end = pygame.time.get_ticks() + 10000
        self.is_shielded = True
        
    def update(self):
        keys = pygame.key.get_pressed()
        # Apply ship-specific speed bonus
        base_speed = 5
        ship_stats = self.get_ship_stats()
        speed = base_speed + ship_stats['speed_bonus']
        
        # Movement and animation
        self.is_moving = False
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= speed
            self.facing_right = False
            self.is_moving = True
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += speed
            self.facing_right = True
            self.is_moving = True
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= speed
            self.is_moving = True
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT:
            self.rect.y += speed
            self.is_moving = True
        
        # Update animation only when moving
        if self.is_moving and len(self.animation_frames) > 1:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_speed:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
        
        # Apply current frame with direction
        if len(self.animation_frames) > 0:
            current_frame = self.animation_frames[self.frame_index]
            if not self.facing_right:
                self.image = pygame.transform.flip(current_frame, True, False)
            else:
                self.image = current_frame
        
        # Update powerup timers
        now = pygame.time.get_ticks()
        if now >= self.shield_end:
            self.is_shielded = False
        
        # Apply shield visual effect
        if self.is_shielded:
            # Make ship semi-transparent when shielded
            self.image.set_alpha(128)

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
            self.speed_x = random.randrange(-2, 2)  # Reset horizontal speed too

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

class SmallProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img, angle):
        super().__init__()
        # Make small projectile
        small_img = pygame.transform.scale(bullet_img, (8, 16))
        self.image = small_img
        self.rect = self.image.get_rect(centerx=x, centery=y)
        
        # Calculate velocity based on angle
        import math
        speed = 8
        self.speed_x = math.cos(math.radians(angle)) * speed
        self.speed_y = math.sin(math.radians(angle)) * speed - 5  # Upward bias

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if (self.rect.bottom < 0 or self.rect.left < 0 or 
            self.rect.right > WIDTH or self.rect.top > HEIGHT):
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

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type, powerup_images):
        super().__init__()
        self.powerup_type = powerup_type
        self.image = powerup_images[powerup_type]
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.speed_y = 2
        self.radius = 20
        
        # Animation for floating effect
        self.float_offset = 0
        self.float_speed = 0.1
        self.float_direction = 1
        self.max_float = 10
        
    def update(self):
        # Move down
        self.rect.y += self.speed_y
        
        # Floating animation
        self.float_offset += self.float_speed * self.float_direction
        if self.float_offset >= self.max_float or self.float_offset <= -self.max_float:
            self.float_direction *= -1
            
        # Remove if off screen
        if self.rect.top > HEIGHT:
            self.kill()

# -- Main Game Loop --
def game_loop(screen, clock, assets, selected_ship=0):
    # Import menu settings
    import menu
    
    # Initialize high score manager
    highscore_manager = HighScoreManager()
    
    # Setup
    game_assets_folder = os.path.join("Assets", "PixelSpaceRage", "256px")
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    small_projectiles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    player = Player(game_assets_folder)
    player.current_ship_index = selected_ship  # Set the initial ship from menu
    player.load_ship_animations()  # Reload the animations with the selected ship
    all_sprites.add(player)
    
    # Load sound effects
    try:
        destroy_sound = pygame.mixer.Sound(os.path.join("Assets", "Destroyed.mp3"))
    except:
        destroy_sound = None
    
    # Load powerup images
    powerup_images = {}
    powerup_types = ['Ammo', 'Energy', 'Health', 'Rocket', 'Shield']
    for ptype in powerup_types:
        try:
            img_path = os.path.join(game_assets_folder, f"Powerup_{ptype}_png_processed.png")
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (40, 40))
            powerup_images[ptype] = img
        except:
            # Fallback powerup image
            fallback = pygame.Surface((40, 40))
            fallback.fill((255, 255, 0))  # Yellow square
            powerup_images[ptype] = fallback
    
    # Load health icon (small ship image)
    def load_health_icon():
        current_ship = player.ship_types[player.current_ship_index]
        try:
            health_icon_path = os.path.join(game_assets_folder, f"Cover_{current_ship}_png_processed.png")
            health_icon = pygame.image.load(health_icon_path).convert_alpha()
            health_icon = pygame.transform.scale(health_icon, (30, 30))
            return health_icon
        except:
            return None
    
    health_icon = load_health_icon()
    
    def spawn_new_block():
        block = Block(assets['meteor_images'])
        all_sprites.add(block)
        enemies.add(block)
    
    def spawn_powerup():
        if random.randint(1, 100) <= 15:  # 15% chance
            ptype = random.choice(powerup_types)
            x = random.randint(50, WIDTH - 50)
            powerup = Powerup(x, -50, ptype, powerup_images)
            all_sprites.add(powerup)
            powerups.add(powerup)
    
    def create_screen_explosion():
        """Create explosions across the screen for Energy powerup"""
        for i in range(15):  # Multiple explosions
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            expl = Explosion((x, y), assets['explosion_anim'])
            all_sprites.add(expl)

    for _ in range(8):
        spawn_new_block()

    score = 0
    game_sub_state = "PLAYING" # "PLAYING", "PAUSED", "GAME_OVER", "HIGH_SCORE_INPUT"
    last_powerup_spawn = 0
    powerup_spawn_delay = 3000  # 3 seconds
    energy_clear_end = 0
    
    # Asteroid spawn management
    last_asteroid_spawn = 0
    asteroid_spawn_delay = 2000  # 2 seconds
    min_asteroids = 6  # Minimum number of asteroids on screen
    
    # High score management
    high_score_processed = False

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
                    # Check shooting cooldown
                    if player.can_shoot():
                        bullet = Bullet(player.rect.centerx, player.rect.top, assets['bullet_img'])
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        player.shoot()  # Record the shot
                if game_sub_state == "GAME_OVER" and event.key == pygame.K_r:
                    return "PLAYING" # Kembali ke main.py untuk restart
                if game_sub_state == "GAME_OVER" and event.key == pygame.K_x:
                    return "MENU" # Kembali ke menu
                if game_sub_state == "HIGH_SCORE_INPUT" and event.key == pygame.K_ESCAPE:
                    game_sub_state = "GAME_OVER"  # Skip name input
                if game_sub_state == "PLAYING" and event.key == pygame.K_p:
                    game_sub_state = "PAUSED"
                    pygame.mixer.music.pause()
                elif game_sub_state == "PAUSED" and event.key == pygame.K_p:
                    game_sub_state = "PLAYING"
                    pygame.mixer.music.unpause()

        # Update
        if game_sub_state == "HIGH_SCORE_INPUT" and not high_score_processed:
            # Handle high score input
            player_name = input_name_screen(screen, clock, score)
            if player_name:
                highscore_manager.add_score(player_name, score)
            high_score_processed = True
            game_sub_state = "GAME_OVER"
        elif game_sub_state == "PLAYING":
            all_sprites.update()
            
            # Spawn powerups occasionally
            now = pygame.time.get_ticks()
            if now - last_powerup_spawn > powerup_spawn_delay:
                spawn_powerup()
                last_powerup_spawn = now
            
            # Maintain minimum asteroids
            if now - last_asteroid_spawn > asteroid_spawn_delay:
                current_asteroid_count = len(enemies)
                if current_asteroid_count < min_asteroids:
                    spawn_new_block()
                    last_asteroid_spawn = now
            
            # Energy powerup effect - clear enemies
            if now < energy_clear_end:
                for enemy in enemies:
                    expl = Explosion(enemy.rect.center, assets['explosion_anim'])
                    all_sprites.add(expl)
                    score += 25  # Bonus for energy clear
                    enemy.kill()
                    spawn_new_block()
                
            # Enemy-Bullet collisions
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 50
                hit_pos = hit.rect.center
                expl = Explosion(hit_pos, assets['explosion_anim'])
                all_sprites.add(expl)
                spawn_new_block()
                
                # Rocket powerup effect - create small projectiles
                if now < player.rocket_boost_end:
                    for angle in [225, 270, 315]:  # Left-up, up, right-up
                        small_proj = SmallProjectile(hit_pos[0], hit_pos[1], assets['bullet_img'], angle)
                        all_sprites.add(small_proj)
                        small_projectiles.add(small_proj)
            
            # Small projectile-Enemy collisions
            small_hits = pygame.sprite.groupcollide(enemies, small_projectiles, True, True)
            for hit in small_hits:
                score += 25
                expl = Explosion(hit.rect.center, assets['explosion_anim'])
                all_sprites.add(expl)
                spawn_new_block()
            
            # Player-Enemy collisions
            hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
            if hits:
                if player.take_damage():  # Check if player dies
                    if destroy_sound:
                        destroy_sound.play()
                    player_expl = Explosion(player.rect.center, assets['explosion_anim'])
                    all_sprites.add(player_expl)
                    player.kill()
                    pygame.mixer.music.stop()
                    
                    # Check if it's a high score
                    if highscore_manager.is_high_score(score):
                        game_sub_state = "HIGH_SCORE_INPUT"
                    else:
                        game_sub_state = "GAME_OVER"
            
            # Player-Powerup collisions
            powerup_hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
            for powerup in powerup_hits:
                score += 25  # Bonus points for collecting powerup
                expl = Explosion(powerup.rect.center, assets['explosion_anim'])
                all_sprites.add(expl)
                
                # Apply powerup effects
                if powerup.powerup_type == 'Ammo':
                    player.activate_ammo_boost()
                elif powerup.powerup_type == 'Energy':
                    energy_clear_end = now + 2000  # 2 seconds
                    create_screen_explosion()
                elif powerup.powerup_type == 'Health':
                    player.heal()
                elif powerup.powerup_type == 'Rocket':
                    player.activate_rocket_boost()
                elif powerup.powerup_type == 'Shield':
                    player.activate_shield()

        elif game_sub_state == "GAME_OVER":
            all_sprites.update() # Hanya update ledakan dll

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 30, WIDTH / 2, 10)
        
        # Draw health indicators
        for i in range(player.health):
            health_x = WIDTH - 80 + (i * 35)
            health_y = HEIGHT - 45
            if health_icon:
                screen.blit(health_icon, (health_x, health_y))
            else:
                # Fallback to rectangle if image fails to load
                health_icon_rect = pygame.Rect(health_x, health_y, 30, 30)
                pygame.draw.rect(screen, (0, 255, 0), health_icon_rect)
        
        # Draw powerup timers
        timer_y = HEIGHT - 40
        if player.is_shielded:
            shield_time = max(0, (player.shield_end - pygame.time.get_ticks()) // 1000)
            draw_text(screen, f"Shield: {shield_time}s", 20, 80, timer_y)
        
        if pygame.time.get_ticks() < player.ammo_boost_end:
            ammo_time = max(0, (player.ammo_boost_end - pygame.time.get_ticks()) // 1000)
            draw_text(screen, f"Ammo: {ammo_time}s", 20, 80, timer_y - 25)
            
        if pygame.time.get_ticks() < player.rocket_boost_end:
            rocket_time = max(0, (player.rocket_boost_end - pygame.time.get_ticks()) // 1000)
            draw_text(screen, f"Rocket: {rocket_time}s", 20, 80, timer_y - 50)
        
        # Apply brightness overlay
        if menu.settings['brightness'] < 1.0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(int((1.0 - menu.settings['brightness']) * 255))
            screen.blit(overlay, (0, 0))
        
        if game_sub_state == "PAUSED":
            draw_text(screen, "Game Paused", 48, WIDTH / 2, HEIGHT / 2 - 50)
            draw_text(screen, "Press P to Continue", 22, WIDTH / 2, HEIGHT / 2)
        elif game_sub_state == "HIGH_SCORE_INPUT":
            # This state is handled in the update section with input_name_screen
            pass
        elif game_sub_state == "GAME_OVER":
            draw_text(screen, "GAME OVER!", 64, WIDTH / 2, HEIGHT / 4)
            draw_text(screen, f"Final Score: {score}", 30, WIDTH / 2, HEIGHT / 2 - 50)
            draw_text(screen, "Press R to restart the game", 30, WIDTH / 2, HEIGHT / 2)
            draw_text(screen, "Press X to exit to main menu", 22, WIDTH / 2, HEIGHT / 2 + 50)

        pygame.display.flip()
