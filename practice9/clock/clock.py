import pygame
import datetime


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.center = (WIDTH // 2, HEIGHT // 2)

        try:
            self.mickey = pygame.image.load("images/image.png").convert_alpha()
            self.right_hand = pygame.image.load("images/1.png").convert_alpha()
            self.left_hand = pygame.image.load("images/2.png").convert_alpha()
        except pygame.error as e:
            print(f"Couldn't load images: {e}")
            pygame.quit()
            exit()

     
        self.mickey = pygame.transform.scale(self.mickey, (600, 600))
       
        self.right_hand = pygame.transform.scale(self.right_hand, (350, 50)) 
        self.left_hand = pygame.transform.scale(self.left_hand, (350, 45))

    def get_angles(self):
        now = datetime.datetime.now()
        
        second_angle = -(now.second * 6) + 90
        minute_angle = -(now.minute * 6) + 90
        return minute_angle, second_angle

    def blit_rotate_center(self, surf, image, pos, angle):
        """Rotates an image around its center and blits it."""
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=pos).center)
        self.screen.blit(rotated_image, new_rect)

    def draw(self):
        self.screen.fill((255, 255, 255)) 
        
        minute_angle, second_angle = self.get_angles()

      
        mickey_rect = self.mickey.get_rect(center=self.center)
        self.screen.blit(self.mickey, mickey_rect)

        
        self.blit_rotate_center(self.screen, self.right_hand, (self.center[0] - 175, self.center[1] - 25), minute_angle)
        self.blit_rotate_center(self.screen, self.left_hand, (self.center[0] - 150, self.center[1] - 22), second_angle)

    
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 8)


mickey_clock = MickeyClock(screen)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey_clock.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()