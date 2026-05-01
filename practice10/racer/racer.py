import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# ================= SETTINGS =================
WIDTH, HEIGHT = 400, 600
FPS = 60

# Границы дороги (подстрой под свою картинку)
ROAD_LEFT = 80
ROAD_RIGHT = 320

# ================= HELPERS =================
def scale_image(image, scale):
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    return pygame.transform.scale(image, (width, height))

# ================= GAME =================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Racer Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)

        # ===== Load images =====
        self.player_img = pygame.image.load("images/racer.png").convert_alpha()
        self.enemy_img = pygame.image.load("images/enemy.png").convert_alpha()
        self.coin_img = pygame.image.load("images/coin.png").convert_alpha()
        self.road_img = pygame.image.load("images/road.png").convert()

        # ===== Scale images (БЕЗ ИСКАЖЕНИЯ) =====
# ===== Scale images (БЕЗ ИСКАЖЕНИЯ) =====
        self.player_img = scale_image(self.player_img, 0.12)
        self.enemy_img = scale_image(self.enemy_img, 0.20)
        self.coin_img = scale_image(self.coin_img, 0.07)
        self.road_img = pygame.transform.scale(self.road_img, (WIDTH, HEIGHT))

        # ===== Sounds =====
        pygame.mixer.music.load("musics/background.mp3")
        pygame.mixer.music.play(-1)

        self.coin_sound = pygame.mixer.Sound("musics/coin.mp3")

        # ===== Objects =====
        self.player = Player(self.player_img)
        self.enemy = Enemy(self.enemy_img)
        self.coins = [Coin(self.coin_img) for _ in range(3)]

        self.score = 0

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.player.move()
        self.enemy.move()

        for coin in self.coins:
            coin.move()

        # ===== Collision: enemy =====
        # Используем hitbox вместо rect
        if self.player.hitbox.colliderect(self.enemy.hitbox):
            print("GAME OVER")
            pygame.quit()
            sys.exit()

        # ===== Collision: coins =====
        # Используем hitbox игрока, чтобы собирать монеты точнее
        for coin in self.coins:
            if self.player.hitbox.colliderect(coin.rect): # Если у монет нет hitbox, используем их rect
                self.score += 1
                self.coin_sound.play()
                coin.spawn()

    def draw(self):
        self.screen.blit(self.road_img, (0, 0))

        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)

        for coin in self.coins:
            self.screen.blit(coin.image, coin.rect)

        # ===== Score =====
        text = self.font.render(f"Coins: {self.score}", True, (0, 0, 0))
        self.screen.blit(text, (WIDTH - 130, 10))

        pygame.display.update()


# ================= PLAYER =================
class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 80))

        # уменьшаем хитбокс
        self.hitbox = self.rect.inflate(-30, -30)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed

        # обновляем хитбокс
        self.hitbox.center = self.rect.center


# ================= ENEMY =================
class Enemy:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5

        self.spawn()  # вызываем после создания rect

        self.hitbox = self.rect.inflate(-30, -30)

    def spawn(self):  # ← ВАЖНО: внутри класса!
        x = random.randint(
            ROAD_LEFT + self.rect.width // 2,
            ROAD_RIGHT - self.rect.width // 2
        )
        self.rect.center = (x, -100)

    def move(self):
        self.rect.y += self.speed
        self.hitbox.center = self.rect.center

        if self.rect.top > HEIGHT:
            self.spawn()


# ================= COIN =================
class Coin:
    def __init__(self, image):
        self.image = image
        self.spawn()

    def spawn(self):
        rect = self.image.get_rect()
        x = random.randint(
            ROAD_LEFT + rect.width // 2,
            ROAD_RIGHT - rect.width // 2
        )
        self.rect = rect
        self.rect.center = (x, -20)
        self.speed = random.randint(3, 6)

    def move(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.spawn()