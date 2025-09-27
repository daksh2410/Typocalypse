import pygame
import random
import os

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Typocalypse")
clock = pygame.time.Clock()

font = pygame.font.SysFont('Consolas', 32)
input_font = pygame.font.SysFont('Consolas', 40, bold=True)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_RED = (100, 0, 0)

LIVES_FONT_PATH = os.path.join("assets", "DeadlyFont.otf")
lives_display_font = None
LIVES_FONT_SIZE = 40

try:
    lives_display_font = pygame.font.Font(LIVES_FONT_PATH, LIVES_FONT_SIZE)
    print(f"Custom font '{LIVES_FONT_PATH}' for lives loaded successfully.")
except FileNotFoundError:
    print(f"Warning: Custom font '{LIVES_FONT_PATH}' not found. Falling back to default font for lives.")
    lives_display_font = pygame.font.SysFont('Consolas', LIVES_FONT_SIZE, bold=True)
except Exception as e:
    print(f"Error loading custom font '{LIVES_FONT_PATH}': {e}. Falling back to default font for lives.")
    lives_display_font = pygame.font.SysFont('Consolas', LIVES_FONT_SIZE, bold=True)

GAME_TITLE_FONT_PATH = os.path.join("assets", "DeadlyFont.otf")
game_title_font = None
GAME_TITLE_FONT_SIZE_PUNISHER = 90
GAME_TITLE_FONT_SIZE_ZOMBIE_KILLER = 50

try:
    game_title_font = pygame.font.Font(GAME_TITLE_FONT_PATH, GAME_TITLE_FONT_SIZE_PUNISHER)
    print(f"Custom font '{GAME_TITLE_FONT_PATH}' for title loaded successfully.")
except FileNotFoundError:
    print(f"Warning: Custom font '{GAME_TITLE_FONT_PATH}' not found. Falling back to default font for title.")
    game_title_font = pygame.font.SysFont('Consolas', GAME_TITLE_FONT_SIZE_PUNISHER, bold=True)
except Exception as e:
    print(f"Error loading custom font '{GAME_TITLE_FONT_PATH}': {e}. Falling back to default font for title.")
    game_title_font = pygame.font.SysFont('Consolas', GAME_TITLE_FONT_SIZE_PUNISHER, bold=True)


backgrounds = []
for i in range(3):
    try:
        img = pygame.image.load(os.path.join("assets", f"background_{i}.png")).convert()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        backgrounds.append(img)
    except FileNotFoundError:
        print(f"Warning: background_{i}.png not found. It will be skipped.")

if not backgrounds:
    default_bg = pygame.Surface((WIDTH, HEIGHT))
    default_bg.fill((20, 20, 20))
    backgrounds.append(default_bg)

current_bg_index = 0
background_img = backgrounds[current_bg_index]

custom_start_screen_bg = None
try:
    temp_img = pygame.image.load(os.path.join("assets", "start_screen_bg.png")).convert()
    custom_start_screen_bg = temp_img
except FileNotFoundError:
    print("Warning: start_screen_bg.png not found. Using default black background for start screen.")

start_screen_img = pygame.Surface((WIDTH, HEIGHT))
start_screen_img.fill(BLACK)
game_over_img = pygame.Surface((WIDTH, HEIGHT))
game_over_img.fill(DARK_RED)

try:
    pygame.mixer.music.load(os.path.join("assets", "game_music.mp3"))
    print("Music loaded successfully.")
except pygame.error:
    print("Error: game_music.mp3 not found or could not be loaded. Music will not play.")

VOLUME_ICON_SIZE = 48
volume_on_icon = None
volume_off_icon = None
try:
    temp_on = pygame.image.load(os.path.join("assets", "icon_volume_on.png")).convert_alpha()
    volume_on_icon = pygame.transform.scale(temp_on, (VOLUME_ICON_SIZE, VOLUME_ICON_SIZE))
    temp_off = pygame.image.load(os.path.join("assets", "icon_volume_off.png")).convert_alpha()
    volume_off_icon = pygame.transform.scale(temp_off, (VOLUME_ICON_SIZE, VOLUME_ICON_SIZE))
except FileNotFoundError:
    print("Warning: Volume icons not found. Mute button will not be fully functional visually.")

is_muted = False


PLAYER_IDLE_IMG = pygame.image.load(os.path.join("assets", "player_idle.png")).convert_alpha()
PLAYER_SHOOT_IMGS = [
    pygame.image.load(os.path.join("assets", "player_shoot_0.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets", "player_shoot_1.png")).convert_alpha(),
    pygame.image.load(os.path.join("assets", "player_shoot_2.png")).convert_alpha()
]

ZOMBIE_SHAMBLER_IMG = pygame.image.load(os.path.join("assets", "zombie_shambler.png")).convert_alpha()
ZOMBIE_BLOATER_IMG = pygame.image.load(os.path.join("assets", "zombie_bloater.png")).convert_alpha()
ZOMBIE_BRUTE_IMG = pygame.image.load(os.path.join("assets", "zombie_brute.png")).convert_alpha()

WORDS_EASY = ["GUTS", "BITE", "CLAW", "FEAST", "DEAD", "SLOW", "DOOM", "FEAR", "GRIM", "PAIN", "TOMB", "DUSK", "GORE"]
WORDS_MEDIUM = ["ZOMBIE", "HORDE", "GROWL", "UNDEAD", "NIGHT", "INFECT", "SHADOW", "CURSED", "CORPSE", "GRAVEY", "FRIGHT", "SCREAM", "DEMON"]
WORDS_HARD = ["SURVIVAL", "INFECTED", "QUARANTINE", "APOCALYPSE", "NIGHTMARE", "OBLIVION", "CEMETERY", "GHASTLY", "MACABRE", "HORRIFIC"]
ALL_WORDS = WORDS_EASY + WORDS_MEDIUM + WORDS_HARD

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_image = pygame.transform.scale(PLAYER_IDLE_IMG, (200, 200))
        self.shoot_frames = [pygame.transform.scale(img, (200, 200)) for img in PLAYER_SHOOT_IMGS]
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=(150, HEIGHT - 100))
        self.is_shooting = False
        self.shoot_frame = 0
        self.shoot_animation_speed = 0.3

    def shoot(self):
        self.is_shooting = True
        self.shoot_frame = 0

    def update(self):
        if self.is_shooting:
            self.shoot_frame += self.shoot_animation_speed
            if self.shoot_frame >= len(self.shoot_frames):
                self.is_shooting = False
                self.image = self.idle_image
            else:
                self.image = self.shoot_frames[int(self.shoot_frame)]
        else:
            self.image = self.idle_image

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.word = random.choice(ALL_WORDS)
        word_len = len(self.word)

        if word_len <= 5:
            base_image = ZOMBIE_SHAMBLER_IMG
            base_size = (100, 120)
            self.speed = random.uniform(0.5, 1.5)
            random_scale = random.uniform(0.9, 1.1)
        elif word_len <= 7:
            base_image = ZOMBIE_BLOATER_IMG
            base_size = (130, 150)
            self.speed = random.uniform(0.8, 1.8)
            random_scale = random.uniform(1.0, 1.2)
        else:
            base_image = ZOMBIE_BRUTE_IMG
            base_size = (160, 180)
            self.speed = random.uniform(1.2, 2.2)
            random_scale = random.uniform(1.1, 1.3)
            
        scaled_image = pygame.transform.scale(base_image, base_size)
        final_w = int(scaled_image.get_width() * random_scale)
        final_h = int(scaled_image.get_height() * random_scale)
        self.image = pygame.transform.scale(scaled_image, (final_w, final_h))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(50, 200)

        ground_zone_top = HEIGHT - 200
        ground_zone_bottom = HEIGHT - 20
        self.rect.bottom = random.randint(ground_zone_top, ground_zone_bottom)


    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    def draw_word(self, surface):
        word_surface = font.render(self.word, True, WHITE)
        word_rect = word_surface.get_rect(center=(self.rect.centerx, self.rect.top - 20))
        surface.blit(word_surface, word_rect)

def game_loop():
    global is_muted
    score = 0
    lives = 3
    active_input = ""
    
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    zombies = pygame.sprite.Group()

    zombie_spawn_timer = 0
    zombie_spawn_rate = 180
    
    running = True

    if pygame.mixer.get_init():
        if not is_muted:
            pygame.mixer.music.play(-1)

    score_y_pos = 10
    score_font_height = font.get_height()
    volume_button_rect = pygame.Rect(10, score_y_pos + score_font_height + 5, VOLUME_ICON_SIZE, VOLUME_ICON_SIZE)

    LIVES_VERTICAL_OFFSET = 5


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    active_input = active_input[:-1]
                elif event.key == pygame.K_RETURN:
                    active_input = ""
                elif event.unicode.isalpha():
                    active_input += event.unicode.upper()
                    player.shoot()
                    for zombie in zombies:
                        if zombie.word == active_input:
                            zombie.kill()
                            score += len(zombie.word)
                            active_input = ""
                            break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volume_button_rect.collidepoint(event.pos):
                    if pygame.mixer.get_init():
                        is_muted = not is_muted
                        if is_muted:
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(1)

        all_sprites.update()
        zombies.update()

        zombie_spawn_timer += 1
        if zombie_spawn_timer >= zombie_spawn_rate and len(zombies) < 10:
            zombies.add(Zombie())
            zombie_spawn_timer = 0
            if zombie_spawn_rate > 60:
                zombie_spawn_rate -= 5

        for zombie in list(zombies):
            if zombie.rect.left < 100:
                zombie.kill()
                lives -= 1
                if lives <= 0:
                    running = False
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                    return "GAME_OVER", score

        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        zombies.draw(screen)

        for zombie in zombies:
            zombie.draw_word(screen)

        pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 200, HEIGHT - 70, 400, 50))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 200, HEIGHT - 70, 400, 50), 3)
        input_surface = input_font.render(active_input, True, GREEN)
        input_rect = input_surface.get_rect(center=(WIDTH // 2, HEIGHT - 45))
        screen.blit(input_surface, input_rect)
        
        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))
        
        lives_text_surface = lives_display_font.render("Lives", True, RED)
        lives_num_display_text = f":{lives}"
        lives_num_surface = font.render(lives_num_display_text, True, RED)
        
        combined_width = lives_text_surface.get_width() + lives_num_surface.get_width()
        start_x = WIDTH - 20 - combined_width
        
        lives_text_rect = lives_text_surface.get_rect(topleft=(start_x, 10 + LIVES_VERTICAL_OFFSET))
        lives_num_rect = lives_num_surface.get_rect(midleft=(lives_text_rect.topright[0], lives_text_rect.midleft[1]))
        
        screen.blit(lives_text_surface, lives_text_rect)
        screen.blit(lives_num_surface, lives_num_rect)

        if pygame.mixer.get_init():
            pygame.draw.rect(screen, (50, 50, 50), volume_button_rect)
            pygame.draw.rect(screen, RED, volume_button_rect, 1)

            if is_muted and volume_off_icon:
                screen.blit(volume_off_icon, volume_button_rect.topleft)
            elif not is_muted and volume_on_icon:
                screen.blit(volume_on_icon, volume_button_rect.topleft)


        pygame.display.flip()
        clock.tick(60)
    
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    return "MENU"

def main_menu():
    start_game_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50)
    settings_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 120, 200, 50)

    while True:
        if custom_start_screen_bg:
            bg_width, bg_height = custom_start_screen_bg.get_size()
            screen_aspect = WIDTH / HEIGHT
            bg_aspect = bg_width / bg_height

            scaled_bg = None
            if screen_aspect > bg_aspect:
                new_height = HEIGHT
                new_width = int(new_height * bg_aspect)
                scaled_bg = pygame.transform.scale(custom_start_screen_bg, (new_width, new_height))
            else:
                new_width = WIDTH
                new_height = int(new_width / bg_aspect)
                scaled_bg = pygame.transform.scale(custom_start_screen_bg, (new_width, new_height))
            
            bg_x = (WIDTH - scaled_bg.get_width()) // 2
            bg_y = (HEIGHT - scaled_bg.get_height()) // 2
            screen.blit(scaled_bg, (bg_x, bg_y))
        else:
            screen.blit(start_screen_img, (0, 0))

        punisher_surface = game_title_font.render("PUNISHER", True, RED)
        punisher_rect = punisher_surface.get_rect(center=(WIDTH / 2 - 30, HEIGHT / 2 - 130))

        subtitle_font = pygame.font.SysFont('Consolas', GAME_TITLE_FONT_SIZE_ZOMBIE_KILLER, bold=True)
        zombie_killer_surface = subtitle_font.render("ZOMBIE KILLER", True, WHITE)
        zombie_killer_rect = zombie_killer_surface.get_rect(midtop=(punisher_rect.centerx, punisher_rect.bottom + 10))

        screen.blit(punisher_surface, punisher_rect)
        screen.blit(zombie_killer_surface, zombie_killer_rect)

        pygame.draw.rect(screen, DARK_RED, start_game_button)
        pygame.draw.rect(screen, DARK_RED, settings_button)
        start_game_text = font.render("Start Game", True, WHITE)
        settings_text = font.render("Settings", True, WHITE)
        screen.blit(start_game_text, start_game_text.get_rect(center=start_game_button.center))
        screen.blit(settings_text, settings_text.get_rect(center=settings_button.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.collidepoint(event.pos):
                    return "PLAY"
                if settings_button.collidepoint(event.pos):
                    return "SETTINGS"

        pygame.display.flip()

def settings_menu():
    global current_bg_index, background_img
    
    button_height = 60
    button_width = 400
    button_padding = 20
    total_height = (button_height + button_padding) * len(backgrounds)
    start_y = (HEIGHT - total_height) / 2

    bg_buttons = []
    for i, bg in enumerate(backgrounds):
        y_pos = start_y + i * (button_height + button_padding)
        button_rect = pygame.Rect(WIDTH / 2 - button_width / 2, y_pos, button_width, button_height)
        bg_buttons.append(button_rect)

    back_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT - 100, 200, 50)

    while True:
        screen.blit(backgrounds[current_bg_index], (0, 0))
        
        for i, button in enumerate(bg_buttons):
            color = GREEN if i == current_bg_index else DARK_RED
            pygame.draw.rect(screen, color, button)
            button_text = font.render(f"Background {i + 1}", True, WHITE)
            screen.blit(button_text, button_text.get_rect(center=button.center))

        pygame.draw.rect(screen, DARK_RED, back_button)
        back_text = font.render("Back", True, WHITE)
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "MENU"
                for i, button in enumerate(bg_buttons):
                    if button.collidepoint(event.pos):
                        current_bg_index = i
                        background_img = backgrounds[current_bg_index]

        pygame.display.flip()


def game_over_screen(current_score, high_score):
    while True:
        screen.blit(game_over_img, (0, 0))
        title_text = input_font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Your Score: {current_score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, GREEN)
        prompt_text = font.render("Press ENTER to Return to Menu", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 80)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
        screen.blit(high_score_text, high_score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 40)))
        screen.blit(prompt_text, prompt_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 120)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "MENU"

if __name__ == '__main__':
    game_state = "MENU"
    high_score = 0
    current_score = 0
    
    while True:
        if game_state == "MENU":
            game_state = main_menu()
        elif game_state == "SETTINGS":
            game_state = settings_menu()
        elif game_state == "PLAY":
            result = game_loop()
            if isinstance(result, tuple):
                game_state, current_score = result
                if current_score > high_score:
                    high_score = current_score
            else:
                game_state = result
        elif game_state == "GAME_OVER":
            game_state = game_over_screen(current_score, high_score)
        elif game_state == "QUIT":
            break

    pygame.quit()