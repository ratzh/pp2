import pygame
import random
import sys

# ================= НАСТРОЙКИ =================
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 240

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game: Levels & Speed")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

# ================= ФУНКЦИИ =================
def generate_food(snake_body):
    """Генерирует еду в случайном месте, проверяя, чтобы она не была на змейке."""
    while True:
        # Случайная позиция, кратная BLOCK_SIZE
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        # Если позиция не занята телом змейки, возвращаем её
        if [x, y] not in snake_body:
            return [x, y]

def draw_stats(score, level):
    """Рисует текущий счет и уровень на экране."""
    stats = font.render(f"Score: {score} | Level: {level}", True, BLACK)
    screen.blit(stats, (10, 10))

# ================= ИГРА =================
def main():
    # Начальное состояние
    snake = [[100, 100], [80, 100], [60, 100]] # Тело змейки
    direction = [BLOCK_SIZE, 0] # Начальное движение вправо
    food = generate_food(snake)
    
    score = 0
    foods_eaten = 0
    level = 1
    speed = 8 # Начальная скорость

    while True:
        # 1. Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction[0] == 0: direction = [-BLOCK_SIZE, 0]
                if event.key == pygame.K_RIGHT and direction[0] == 0: direction = [BLOCK_SIZE, 0]
                if event.key == pygame.K_UP and direction[1] == 0: direction = [0, -BLOCK_SIZE]
                if event.key == pygame.K_DOWN and direction[1] == 0: direction = [0, BLOCK_SIZE]
                if event.key == pygame.K_a and direction[0] == 0: direction = [-BLOCK_SIZE, 0]
                if event.key == pygame.K_d and direction[0] == 0: direction = [BLOCK_SIZE, 0]
                if event.key == pygame.K_w and direction[1] == 0: direction = [0, -BLOCK_SIZE]
                if event.key == pygame.K_s and direction[1] == 0: direction = [0, BLOCK_SIZE]

        # 2. Логика движения
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        
        # --- ПРОВЕРКА СТОЛКНОВЕНИЯ СО СТЕНОЙ ---
        if (new_head[0] < 0 or new_head[0] >= WIDTH or 
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            print(f"GAME OVER! Score: {score}")
            pygame.quit()
            sys.exit()

        # --- ПРОВЕРКА СТОЛКНОВЕНИЯ С САМИМ СОБОЙ ---
        if new_head in snake:
            pygame.quit()
            sys.exit()

        snake.insert(0, new_head)

        # 3. Поедание еды
        if new_head == food:
            score += 1
            foods_eaten += 1
            food = generate_food(snake) # Новая еда
            
            # --- УРОВНИ И СКОРОСТЬ ---
            if foods_eaten >= 3: # Каждые 3 еды повышаем уровень
                level += 1
                speed += 2 # Увеличиваем скорость
                foods_eaten = 0 # Сбрасываем счетчик для следующего уровня
        else:
            snake.pop() # Удаляем хвост, если не съели еду

        # 4. Отрисовка
        screen.fill(WHITE)
        
        # Рисуем еду
        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Рисуем змейку
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            
        draw_stats(score, level)
        
        pygame.display.update()
        clock.tick(speed) # Управление скоростью игры

if __name__ == "__main__":
    main()