import pygame
import sys
import os
import random
import core  # Diubah dari 'import game' menjadi 'import core'
import menu

# -- Main Function --
def main():
    pygame.init()
    pygame.mixer.init()

    # -- Constants --
    HEIGHT = 600
    WIDTH = 800
    
    # Setup layar
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()

    # -- Asset Paths --
    assets_folder = "Assets"
    game_assets_folder = os.path.join(assets_folder, "PixelSpaceRage", "256px")

    # -- Load Assets --
    assets = {
        'meteor_images': [],
        'bullet_img': None,
        'explosion_anim': [],
        'background_music': os.path.join(assets_folder, "Background Music.mp3")
    }

    # Memuat gambar-gambar meteor
    meteor_folder = os.path.join(game_assets_folder, "Asteroid")
    for file in os.listdir(meteor_folder):
        if file.endswith(".png"):
            img_path = os.path.join(meteor_folder, file)
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (random.randint(40, 70), random.randint(40, 70)))
            assets['meteor_images'].append(img)

    # Memuat gambar peluru
    bullet_img_path = os.path.join(game_assets_folder, "Laser_Small_png_processed.png")
    assets['bullet_img'] = pygame.image.load(bullet_img_path).convert_alpha()
    assets['bullet_img'] = pygame.transform.scale(assets['bullet_img'], (15, 35))

    # Memuat gambar-gambar untuk animasi ledakan
    for i in range(1, 10):
        filename = f'Explosion02_Frame_0{i}_png_processed.png'
        img_path = os.path.join(game_assets_folder, filename)
        img = pygame.image.load(img_path).convert_alpha()
        img = pygame.transform.scale(img, (80, 80))
        assets['explosion_anim'].append(img)

    # -- Game State Machine --
    game_state = "MENU"
    selected_ship = 0  # Default ship selection
    
    while True:
        if game_state == "MENU":
            if hasattr(menu, 'menu_loop'):
                result = menu.menu_loop(screen, clock)
                if isinstance(result, tuple):
                    game_state, selected_ship = result
                else:
                    game_state = result
            else:
                print("Fungsi menu_loop tidak ditemukan, memulai game secara langsung.")
                game_state = "PLAYING"
        elif game_state == "OPTIONS":
            if hasattr(menu, 'options_loop'):
                game_state = menu.options_loop(screen, clock)
                # Apply music volume setting
                pygame.mixer.music.set_volume(menu.settings['music_volume'])
            else:
                print("Fungsi options_loop tidak ditemukan, kembali ke menu.")
                game_state = "MENU"
        elif game_state == "PLAYING":
            # Diubah dari 'game.game_loop' menjadi 'core.game_loop'
            game_state = core.game_loop(screen, clock, assets, selected_ship)
        
        if game_state == "QUIT":
            break
            
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

