import pygame
import sys

# ================= НАСТРОЙКИ =================
WIDTH, HEIGHT = 800, 600
UI_HEIGHT = 80  # Увеличил высоту панели, чтобы поместились и палитра, и текст

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint Pro: Рисуй, выбирай цвета, используй горячие клавиши!")
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)
    
    # --- Основной холст ---
    drawing_surface = pygame.Surface((WIDTH, HEIGHT))
    drawing_surface.fill(WHITE)
    
    # --- Палитра ---
    palette_surface = pygame.Surface((WIDTH, 40)) # Палитра занимает только верхнюю часть панели
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

            # --- Управление инструментами (Клавиши) ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: current_tool = 'rect'   # R - Rectangle
                if event.key == pygame.K_c: current_tool = 'circle' # C - Circle
                if event.key == pygame.K_p: current_tool = 'pen'    # P - Pen
                if event.key == pygame.K_e: current_tool = 'eraser' # E - Eraser

            # --- Работа мышкой ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Если клик в зоне палитры (первые 40 пикселей сверху)
                if mouse_pos[1] < 40:
                    current_color = palette_surface.get_at(mouse_pos)
                # Если клик ниже палитры - начинаем рисовать
                elif mouse_pos[1] > UI_HEIGHT:
                    is_drawing = True
                    start_pos = mouse_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if is_drawing:
                    if current_tool == 'rect':
                        draw_rect(drawing_surface, current_color, start_pos, mouse_pos)
                    elif current_tool == 'circle':
                        draw_circle(drawing_surface, current_color, start_pos, mouse_pos)
                is_drawing = False

            if event.type == pygame.MOUSEMOTION and is_drawing:
                if current_tool == 'pen':
                    pygame.draw.line(drawing_surface, current_color, start_pos, mouse_pos, 3)
                    start_pos = mouse_pos
                elif current_tool == 'eraser':
                    pygame.draw.circle(drawing_surface, WHITE, mouse_pos, 20)

        # --- ОТРИСОВКА ---
        screen.fill(WHITE)
        screen.blit(drawing_surface, (0, 0))

        # Превью фигур
        if is_drawing and mouse_pos[1] > UI_HEIGHT:
            if current_tool == 'rect':
                draw_rect(screen, current_color, start_pos, mouse_pos)
            elif current_tool == 'circle':
                draw_circle(screen, current_color, start_pos, mouse_pos)

        # Рисуем интерфейс
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, UI_HEIGHT)) # Фон панели
        screen.blit(palette_surface, (0, 0))                    # Радужная палитра
        
        # Рисуем текст-подсказку
        controls_text = f"Tool: {current_tool.upper()} | P: Pen, C: Circle, R: Rect, E: Eraser"
        txt = font.render(controls_text, True, BLACK)
        screen.blit(txt, (10, 50)) # Текст отображается под палитрой

        pygame.display.flip()
        clock.tick(60)

# --- ФУНКЦИИ ---
def draw_rect(surface, color, start, end):
    x, y = min(start[0], end[0]), min(start[1], end[1])
    w, h = abs(start[0] - end[0]), abs(start[1] - end[1])
    pygame.draw.rect(surface, color, (x, y, w, h), 3)

def draw_circle(surface, color, start, end):
    radius = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
    pygame.draw.circle(surface, color, start, radius, 3)

if __name__ == "__main__":
    main()