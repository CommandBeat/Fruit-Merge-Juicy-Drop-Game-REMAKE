import pygame
import random
import os

# --- Setup ---
os.chdir("FMJDGR")  # Ensure this directory exists with correct assets
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Merge: Juicy Drop Game REMAKE")
clock = pygame.time.Clock()
FPS = 60

# --- Assets ---
FRUIT_IMAGES = [
    "images/orange.png", "images/kiwi.png", "images/fejoa.png",
    "images/pomergranite.png", "images/pineapple.png",
    "images/watermelon.png", "images/passionfruit.png", "images/dragonfruit.png"
]
FRUITS = [pygame.image.load(img).convert_alpha() for img in FRUIT_IMAGES]

# --- Colors & Fonts ---
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)

title_font = pygame.font.Font("UbuntuFonts/Ubuntu-Bold.ttf", 50)
instr_font = pygame.font.Font("UbuntuFonts/Ubuntu-Italic.ttf", 20)
score_font = pygame.font.Font("UbuntuFonts/Ubuntu-Bold.ttf", 30)
scr_font = pygame.font.Font("UbuntuFonts/Ubuntu-Regular.ttf", 30)
highscore_font = pygame.font.Font("UbuntuFonts/Ubuntu-Bold.ttf", 30)
game_over_font = pygame.font.Font("UbuntuFonts/Ubuntu-BoldItalic.ttf", 50)

# --- Game Variables ---
game_state = "menu"
gravity = 5
score = 0
highscore = 0
active_fruit = None
fruits = []


# --- Fruit Object ---
class Fruit:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.level = level
        self.image = FRUITS[level]
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = self.rect.width // 2
        self.dy = 0

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self, dt):
        self.dy += gravity * dt
        self.y += self.dy
        self.rect.centery = int(self.y)

    def collide(self, other):
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        return (dx**2 + dy**2)**0.5 < self.radius + other.radius


# --- Utility Functions ---
def spawn_fruit():
    return Fruit(WIDTH // 2, 50, random.randint(0, 1))


def merge_fruits(f1, f2):
    new_level = f1.level + 1
    if new_level >= len(FRUITS):
        return None
    new_x = (f1.x + f2.x) // 2
    new_y = (f1.y + f2.y) // 2
    return Fruit(new_x, new_y, new_level)


# --- Main Loop ---
running = True
while running:
    dt = clock.tick(FPS) / 1000
    screen.fill(CYAN)

    # --- Score Display ---
    score_render = score_font.render(str(score), True, BLUE)
    score_text = scr_font.render("Score:", True, BLUE)
    highscore_render = highscore_font.render(str(highscore), True, BLUE)
    highscore_text = scr_font.render("Highscore:", True, BLUE)

    score_render_rect = score_render.get_rect(topright=(WIDTH - 10, 0))
    score_text_rect = score_text.get_rect(topright=(score_render_rect.left - 5, 0))
    highscore_render_rect = highscore_render.get_rect(topright=(WIDTH - 10, 40))
    highscore_text_rect = highscore_text.get_rect(topright=(highscore_render_rect.left - 5, 40))

    screen.blit(score_text, score_text_rect)
    screen.blit(score_render, score_render_rect)
    screen.blit(highscore_text, highscore_text_rect)
    screen.blit(highscore_render, highscore_render_rect)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # --- Menu ---
    if game_state == "menu":
        title = title_font.render("Fruit Merge: Juicy Drop Game", True, BLUE)
        instr = instr_font.render("(Press E to start)", True, BLUE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))
        screen.blit(instr, instr.get_rect(center=(WIDTH // 2, 160)))
        score = 0
        if keys[pygame.K_e]:
            fruits.clear()
            active_fruit = spawn_fruit()
            game_state = "play"

    # --- Game Over ---
    elif game_state == "game over":
        over = game_over_font.render("GAME OVER!", True, (255, 0, 0))
        instr = instr_font.render("(Press R to restart)", True, (255, 0, 0))
        screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 5)))
        screen.blit(instr, instr.get_rect(center=(WIDTH // 2, HEIGHT // 5 + over.get_height())))
        highscore = max(highscore, score)

    # --- Gameplay ---
    elif game_state == "play":
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and active_fruit.rect.left > 0:
            active_fruit.x -= 300 * dt
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and active_fruit.rect.right < WIDTH:
            active_fruit.x += 300 * dt

        active_fruit.rect.centerx = int(active_fruit.x)
        active_fruit.update(dt)

        if active_fruit.rect.bottom >= HEIGHT:
            active_fruit.rect.bottom = HEIGHT
            fruits.append(active_fruit)
            active_fruit = spawn_fruit()
        else:
            for fruit in fruits:
                if active_fruit.collide(fruit):
                    if active_fruit.level == fruit.level:
                        merged = merge_fruits(active_fruit, fruit)
                        score += 1
                        if merged:
                            fruits.remove(fruit)
                            active_fruit = merged
                        else:
                            active_fruit = spawn_fruit()
                        break
                    else:
                        fruits.append(active_fruit)
                        active_fruit = spawn_fruit()
                        break

        for fruit in fruits:
            if fruit.y <= fruit.rect.height:
                game_state = "game over"
            fruit.draw(screen)

        active_fruit.draw(screen)

    if keys[pygame.K_r]:
        game_state = "menu"

    if score > highscore:
        highscore = score

    pygame.display.flip()

pygame.quit()
