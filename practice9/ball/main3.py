import pygame
import sys
from ball import Ball

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    clock = pygame.time.Clock()
    
  
    ball = Ball(WIDTH, HEIGHT)

    while True:
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    ball.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(1, 0)

      
        screen.fill((255, 255, 255))
        ball.draw(screen)
        
      
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()