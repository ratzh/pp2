import pygame
import random
import sys


WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 240
FOOD_LIFETIME = 5000  # Время жизни еды в миллисекундах (5 секунд)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game: Weighted Food")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

def generate_food(snake_body):
    while True:
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        if [x, y] not in snake_body:
    
            weight = random.choice([1, 2, 3]) 
            color = GREEN if weight == 1 else (ORANGE if weight == 2 else RED)
            return {'pos': [x, y], 'weight': weight, 'color': color}

def draw_stats(score, level):
    stats = font.render(f"Score: {score} | Level: {level}", True, BLACK)
    screen.blit(stats, (10, 10))


def main():
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = [BLOCK_SIZE, 0]
    
    food = generate_food(snake)
    food_spawn_time = pygame.time.get_ticks() 
    
    score = 0
    foods_eaten = 0
    level = 1
    speed = 8 

    while True:
        current_time = pygame.time.get_ticks() 


        if current_time - food_spawn_time > FOOD_LIFETIME:
            food = generate_food(snake)
            food_spawn_time = current_time

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a] and direction[0] == 0: direction = [-BLOCK_SIZE, 0]
                if event.key in [pygame.K_RIGHT, pygame.K_d] and direction[0] == 0: direction = [BLOCK_SIZE, 0]
                if event.key in [pygame.K_UP, pygame.K_w] and direction[1] == 0: direction = [0, -BLOCK_SIZE]
                if event.key in [pygame.K_DOWN, pygame.K_s] and direction[1] == 0: direction = [0, BLOCK_SIZE]

        # 2. Логика движения
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        
        if (new_head[0] < 0 or new_head[0] >= WIDTH or 
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake):
            print(f"GAME OVER! Score: {score}")
            pygame.quit()
            sys.exit()

        snake.insert(0, new_head)

        # 3. Поедание еды
        if new_head == food['pos']:
            score += food['weight']
            foods_eaten += 1
            
            # Обновляем еду и сбрасываем таймер
            food = generate_food(snake)
            food_spawn_time = current_time 
            
            if foods_eaten >= 3:
                level += 1
                speed += 2
                foods_eaten = 0
        else:
            snake.pop()

        # 4. Отрисовка
        screen.fill(WHITE)
        
        # Рисуем еду (используем цвет и позицию из словаря)
        pygame.draw.rect(screen, food['color'], (food['pos'][0], food['pos'][1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Рисуем змейку
        for segment in snake:
            pygame.draw.rect(screen, BLACK, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            
        draw_stats(score, level)
        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    main()