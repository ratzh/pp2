import pygame
import sys
import math

WIDTH, HEIGHT = 800, 600
UI_HEIGHT = 100  

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint Pro: Рисуй фигуры!")
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16, bold=True)
    
    # --- Основной холст ---
    drawing_surface = pygame.Surface((WIDTH, HEIGHT))
    drawing_surface.fill(WHITE)
    
    # --- Палитра ---
    palette_surface = pygame.Surface((WIDTH, 40))
    for x in range(WIDTH):
        r = int(min(255, max(0, 255 - abs(x - WIDTH/3) * 2)))
        g = int(min(255, max(0, 255 - abs(x - WIDTH/2) * 2)))
        b = int(min(255, max(0, 255 - abs(x - WIDTH*0.8) * 2)))
        pygame.draw.line(palette_surface, (r, g, b), (x, 0), (x, 40))

    # Состояние
    current_tool = 'pen'
    current_color = BLACK
    is_drawing = False
    start_pos = None

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: current_tool = 'rect'
                if event.key == pygame.K_c: current_tool = 'circle'
                if event.key == pygame.K_p: current_tool = 'pen'
                if event.key == pygame.K_e: current_tool = 'eraser'
                if event.key == pygame.K_s: current_tool = 'square'
                if event.key == pygame.K_t: current_tool = 'right_tri'
                if event.key == pygame.K_q: current_tool = 'eq_tri'
                if event.key == pygame.K_d: current_tool = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_pos[1] < 40:
                    current_color = palette_surface.get_at(mouse_pos)
                elif mouse_pos[1] > UI_HEIGHT:
                    is_drawing = True
                    start_pos = mouse_pos

            if event.type == pygame.MOUSEBUTTONUP and is_drawing:
                # Вызываем отрисовку при отпускании мыши
                draw_shape(drawing_surface, current_tool, current_color, start_pos, mouse_pos)
                is_drawing = False

            if event.type == pygame.MOUSEMOTION and is_drawing:
                if current_tool == 'pen':
                    pygame.draw.line(drawing_surface, current_color, start_pos, mouse_pos, 3)
                    start_pos = mouse_pos
                elif current_tool == 'eraser':
                    pygame.draw.circle(drawing_surface, WHITE, mouse_pos, 20)

        screen.fill(WHITE)
        screen.blit(drawing_surface, (0, 0))

        # Превью (рисование фигуры в реальном времени при движении мыши)
        if is_drawing and mouse_pos[1] > UI_HEIGHT:
            draw_shape(screen, current_tool, current_color, start_pos, mouse_pos)

        # Интерфейс
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, UI_HEIGHT))
        screen.blit(palette_surface, (0, 0))
        
        controls = f"Tool: {current_tool.upper()} | P:Pen, E:Eraser, R:Rect, C:Circle, S:Square, T:RightTri, Q:EqTri, D:Rhombus"
        txt = font.render(controls, True, BLACK)
        screen.blit(txt, (10, 50))

        pygame.display.flip()
        clock.tick(60)


def draw_shape(surface, tool, color, start, end):
    """Единый диспетчер для отрисовки фигур."""
    if tool == 'rect':
        x, y = min(start[0], end[0]), min(start[1], end[1])
        w, h = abs(start[0] - end[0]), abs(start[1] - end[1])
        pygame.draw.rect(surface, color, (x, y, w, h), 3)
    elif tool == 'circle':
        radius = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
        pygame.draw.circle(surface, color, start, radius, 3)
    elif tool == 'square':
        
        side = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
        x = start[0] if end[0] > start[0] else start[0] - side
        y = start[1] if end[1] > start[1] else start[1] - side
        pygame.draw.rect(surface, color, (x, y, side, side), 3)
    elif tool == 'right_tri':
        
        pygame.draw.polygon(surface, color, [start, (start[0], end[1]), end], 3)
    elif tool == 'eq_tri':
       
        base = abs(end[0] - start[0])
        height = int(base * math.sqrt(3) / 2)
        p1 = (start[0], end[1])
        p2 = (end[0], end[1])
        p3 = (start[0] + (end[0] - start[0]) / 2, end[1] - height)
        pygame.draw.polygon(surface, color, [p1, p2, p3], 3)
    elif tool == 'rhombus':
        
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        points = [
            (mid_x, start[1]), # Верх
            (end[0], mid_y),   # Право
            (mid_x, end[1]),   # Низ
            (start[0], mid_y)  # Лево
        ]
        pygame.draw.polygon(surface, color, points, 3)

if __name__ == "__main__":
    main()