import pygame
import sys
from datetime import datetime


from tools import draw_shape, flood_fill, TextTool, BRUSH_SIZES



WIDTH, HEIGHT = 800, 600
UI_HEIGHT = 100

WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
GRAY       = (210, 210, 210)
DARK_GRAY  = (110, 110, 110)
ACTIVE_CLR = (60,  120, 200)

TOOL_KEYS = {
    pygame.K_p: 'pen',
    pygame.K_l: 'line',
    pygame.K_e: 'eraser',
    pygame.K_f: 'fill',
    pygame.K_x: 'text',
    pygame.K_r: 'rect',
    pygame.K_c: 'circle',
    pygame.K_s: 'square',
    pygame.K_t: 'right_tri',
    pygame.K_q: 'eq_tri',
    pygame.K_d: 'rhombus',
}


SHAPE_TOOLS = {'line', 'rect', 'circle', 'square', 'right_tri', 'eq_tri', 'rhombus'}



def draw_toolbar(screen, font, small_font, current_tool,
                 current_color, brush_size_key, palette_surface):

    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, DARK_GRAY, (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 2)

    # Rainbow palette strip
    screen.blit(palette_surface, (0, 0))


    sx, sy = WIDTH - 65, 5
    pygame.draw.rect(screen, current_color, (sx, sy, 32, 32))
    pygame.draw.rect(screen, BLACK,         (sx, sy, 32, 32), 2)
    lbl = small_font.render("colour", True, BLACK)
    screen.blit(lbl, (sx - 2, sy + 34))

    
    for key in (1, 2, 3):
        bx = WIDTH - 150 + (key - 1) * 30
        by = 5
        active = (brush_size_key == key)
        bg = ACTIVE_CLR if active else (240, 240, 240)
        pygame.draw.rect(screen, bg,    (bx, by, 24, 24))
        pygame.draw.rect(screen, BLACK, (bx, by, 24, 24), 1)
        num = small_font.render(str(key), True, WHITE if active else BLACK)
        screen.blit(num, (bx + 7, by + 4))
    size_lbl = small_font.render("size 1/2/3", True, BLACK)
    screen.blit(size_lbl, (WIDTH - 152, 32))

 
    tool_surf = font.render(f"Tool: {current_tool.upper()}", True, BLACK)
    screen.blit(tool_surf, (10, 46))


    hints = ("P:Pen  L:Line  E:Eraser  F:Fill  X:Text  "
             "R:Rect  C:Circle  S:Square  T:RTri  Q:ETri  D:Rhombus"
             "   |   Ctrl+S: Save")
    screen.blit(small_font.render(hints, True, DARK_GRAY), (10, 70))




def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint Pro")
    clock = pygame.time.Clock()

    font       = pygame.font.SysFont("Arial", 16, bold=True)
    small_font = pygame.font.SysFont("Arial", 12)
    text_font  = pygame.font.SysFont("Arial", 22)


    drawing_surface = pygame.Surface((WIDTH, HEIGHT))
    drawing_surface.fill(WHITE)

    palette_surface = pygame.Surface((WIDTH, 40))
    for x in range(WIDTH):
        r = int(min(255, max(0, 255 - abs(x - WIDTH / 3)   * 2)))
        g = int(min(255, max(0, 255 - abs(x - WIDTH / 2)   * 2)))
        b = int(min(255, max(0, 255 - abs(x - WIDTH * 0.8) * 2)))
        pygame.draw.line(palette_surface, (r, g, b), (x, 0), (x, 40))

  
    current_tool    = 'pen'
    current_color   = BLACK
    brush_size_key  = 1
    is_drawing      = False
    start_pos       = None

    text_tool = TextTool(text_font)

    while True:
        mouse_pos  = pygame.mouse.get_pos()
        brush_size = BRUSH_SIZES[brush_size_key]

        for event in pygame.event.get():

       
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

               
                if text_tool.active:
                    text_tool.handle_key(event)
                    if text_tool.confirmed:
                        text_tool.commit(drawing_surface, current_color)
                        text_tool.reset()
                   
                    continue          

                mods = pygame.key.get_mods()

                
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
                    path = f"canvas_{ts}.png"
                    pygame.image.save(drawing_surface, path)
                    pygame.display.set_caption(f"Paint Pro  —  saved {path}")
                    continue

               
                if event.key == pygame.K_1:   brush_size_key = 1
                elif event.key == pygame.K_2: brush_size_key = 2
                elif event.key == pygame.K_3: brush_size_key = 3

                elif event.key in TOOL_KEYS:
                    current_tool = TOOL_KEYS[event.key]

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = mouse_pos

               
                if my < 40:
                    current_color = palette_surface.get_at((mx, my))[:3]
                    continue

                
                if my > UI_HEIGHT:
                    if current_tool == 'fill':
                        flood_fill(drawing_surface, mouse_pos, current_color)

                    elif current_tool == 'text':
                        text_tool.start(mouse_pos)

                    else:
                        is_drawing = True
                        start_pos  = mouse_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if is_drawing and start_pos:
                    if current_tool in SHAPE_TOOLS:
                        draw_shape(drawing_surface, current_tool,
                                   current_color, start_pos, mouse_pos, brush_size)
                    is_drawing = False
                    start_pos  = None

            if event.type == pygame.MOUSEMOTION and is_drawing:
                if current_tool == 'pen':
                    pygame.draw.line(drawing_surface, current_color,
                                     start_pos, mouse_pos, brush_size)
                    start_pos = mouse_pos
                elif current_tool == 'eraser':
                    pygame.draw.circle(drawing_surface, WHITE,
                                       mouse_pos, brush_size * 4)

       
        screen.fill(WHITE)
        screen.blit(drawing_surface, (0, 0))

        if is_drawing and start_pos and current_tool in SHAPE_TOOLS:
            draw_shape(screen, current_tool, current_color,
                       start_pos, mouse_pos, brush_size)

       
        if current_tool == 'eraser' and mouse_pos[1] > UI_HEIGHT:
            pygame.draw.circle(screen, DARK_GRAY, mouse_pos, brush_size * 4, 1)

        
        text_tool.draw_preview(screen, current_color)

     
        draw_toolbar(screen, font, small_font, current_tool,
                     current_color, brush_size_key, palette_surface)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
