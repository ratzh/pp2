import pygame
import sys
from player import MusicPlayer


WIDTH, HEIGHT = 600, 300
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GREEN = (0, 255, 127)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python Keyboard Music Player")
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    
    player = MusicPlayer("musics")
    
    running = True
    while running:
        screen.fill(BLACK)
        
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    player.play()
                elif event.key == pygame.K_s: 
                    player.stop()
                elif event.key == pygame.K_n: 
                    player.next_track()
                elif event.key == pygame.K_b: 
                    player.prev_track()
                elif event.key == pygame.K_q: 
                    running = False

       
        status = "Playing" if player.is_playing else "Stopped"
        track_text = font.render(f"Track: {player.get_current_track_name()}", True, WHITE)
        status_text = font.render(f"Status: {status}", True, GREEN if player.is_playing else WHITE)
        controls_text = font.render("[P] Play  [S] Stop  [N] Next  [B] Back  [Q] Quit", True, WHITE)

        screen.blit(track_text, (50, 80))
        screen.blit(status_text, (50, 130))
        screen.blit(controls_text, (50, 220))

        
        if player.is_playing:
            pygame.draw.rect(screen, WHITE, (50, 180, 500, 10), 2)
            
            
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()