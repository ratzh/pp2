import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
FPS = 60
ROAD_LEFT = 80
ROAD_RIGHT = 320
SPEED_STEP = 1      # На сколько увеличиваем скорость
N_COINS = 5         # Каждые N монет увеличиваем скорость врага

def scale_image(image, scale):
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    return pygame.transform.scale(image, (width, height))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Racer Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)

    
        self.player_img = pygame.image.load("images/racer.png").convert_alpha()
        self.enemy_img = pygame.image.load("images/enemy.png").convert_alpha()
        self.coin_img = pygame.image.load("images/coin.png").convert_alpha()
        self.road_img = pygame.image.load("images/road.png").convert()

    
        self.player_img = scale_image(self.player_img, 0.12)
        self.enemy_img = scale_image(self.enemy_img, 0.20)
        self.coin_img = scale_image(self.coin_img, 0.07)
        self.road_img = pygame.transform.scale(self.road_img, (WIDTH, HEIGHT))

        pygame.mixer.music.load("musics/background.mp3")
        pygame.mixer.music.play(-1)
        self.coin_sound = pygame.mixer.Sound("musics/coin.mp3")

     
        self.player = Player(self.player_img)
        self.enemy = Enemy(self.enemy_img)
     
        self.coins = [Coin(self.coin_img) for _ in range(3)]

        self.score = 0
        self.total_coins_count = 0  

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

        # Collision: enemy
        if self.player.hitbox.colliderect(self.enemy.hitbox):
            print(f"GAME OVER! Score: {self.score}")
            pygame.quit()
            sys.exit()

        # Collision: coins
        for coin in self.coins:
            if self.player.hitbox.colliderect(coin.rect):
              
                self.score += coin.weight 
                self.total_coins_count += 1
                self.coin_sound.play()
                
                # УСЛОВИЕ: Увеличение скорости врага каждые N собранных монет
                if self.total_coins_count % N_COINS == 0:
                    self.enemy.speed += SPEED_STEP
                    print(f"Speed increased! Current enemy speed: {self.enemy.speed}")
                
                coin.spawn()

    def draw(self):
        self.screen.blit(self.road_img, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)

        for coin in self.coins:
            self.screen.blit(coin.image, coin.rect)
            # (Опционально) Можно рисовать вес монеты рядом с ней для наглядности
            # weight_txt = self.font.render(str(coin.weight), True, (255, 0, 0))
            # self.screen.blit(weight_txt, coin.rect.topleft)


        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        speed_text = self.font.render(f"Enemy Speed: {self.enemy.speed}", True, (200, 0, 0))
        self.screen.blit(text, (WIDTH - 130, 10))
        self.screen.blit(speed_text, (10, 10))

        pygame.display.update()



class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 80))
        self.hitbox = self.rect.inflate(-30, -30)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed
        self.hitbox.center = self.rect.center



class Enemy:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5 
        self.spawn()
        self.hitbox = self.rect.inflate(-30, -30)

    def spawn(self):
        x = random.randint(ROAD_LEFT + self.rect.width // 2, ROAD_RIGHT - self.rect.width // 2)
        self.rect.center = (x, -100)

    def move(self):
        self.rect.y += self.speed
        self.hitbox.center = self.rect.center
        if self.rect.top > HEIGHT:
            self.spawn()


class Coin:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.weight = 1 
        self.spawn()

    def spawn(self):
        
        x = random.randint(ROAD_LEFT + self.rect.width // 2, ROAD_RIGHT - self.rect.width // 2)
        self.rect.center = (x, random.randint(-500, -50)) # Монеты могут спавниться выше для разнообразия
        
    
        weights_pool = [1] * 10 + [3] * 5 + [5] * 2
        self.weight = random.choice(weights_pool)
        

        self.speed = random.randint(3, 6)

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.spawn()

if __name__ == "__main__":
    game = Game()
    game.run()