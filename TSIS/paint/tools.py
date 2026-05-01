import pygame
import math
from collections import deque

WHITE = (255, 255, 255)

BRUSH_SIZES = {1: 2, 2: 5, 3: 10}




def draw_shape(surface, tool, color, start, end, brush_size):
    """Dispatcher for all shape / line tools."""
    t = brush_size

    if tool == 'line':
        pygame.draw.line(surface, color, start, end, t)

    elif tool == 'rect':
        x, y = min(start[0], end[0]), min(start[1], end[1])
        w, h = abs(start[0] - end[0]), abs(start[1] - end[1])
        pygame.draw.rect(surface, color, (x, y, w, h), t)

    elif tool == 'circle':
        radius = int(math.hypot(start[0] - end[0], start[1] - end[1]))
        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, t)

    elif tool == 'square':
        side = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
        x = start[0] if end[0] >= start[0] else start[0] - side
        y = start[1] if end[1] >= start[1] else start[1] - side
        pygame.draw.rect(surface, color, (x, y, side, side), t)

    elif tool == 'right_tri':
        pygame.draw.polygon(surface, color, [start, (start[0], end[1]), end], t)

    elif tool == 'eq_tri':
        base = abs(end[0] - start[0])
        height = int(base * math.sqrt(3) / 2)
        p1 = (start[0], end[1])
        p2 = (end[0], end[1])
        p3 = (start[0] + (end[0] - start[0]) / 2, end[1] - height)
        pygame.draw.polygon(surface, color, [p1, p2, p3], t)

    elif tool == 'rhombus':
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        points = [
            (mid_x, start[1]),
            (end[0],  mid_y),
            (mid_x, end[1]),
            (start[0], mid_y),
        ]
        pygame.draw.polygon(surface, color, points, t)




def flood_fill(surface, start_pos, fill_color):
    """BFS flood-fill on a pygame Surface."""
    sx, sy = int(start_pos[0]), int(start_pos[1])
    w, h = surface.get_size()
    if not (0 <= sx < w and 0 <= sy < h):
        return

    target = surface.get_at((sx, sy))[:3]
    fc = tuple(fill_color[:3])
    if target == fc:
        return

    queue = deque([(sx, sy)])
    visited = {(sx, sy)}

    surface.lock()
    while queue:
        x, y = queue.popleft()
        if surface.get_at((x, y))[:3] != target:
            continue
        surface.set_at((x, y), fc)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    surface.unlock()



class TextTool:
    
    def __init__(self, font):
        self.font = font
        self.active = False
        self.pos = (0, 0)
        self.buffer = ""
        self.confirmed = False  
        self.cancelled = False  

 

    def start(self, pos):
        self.pos = pos
        self.buffer = ""
        self.active = True
        self.confirmed = False
        self.cancelled = False

    def reset(self):
        self.active = False
        self.buffer = ""
        self.confirmed = False
        self.cancelled = False



    def handle_key(self, event):
        
        if not self.active:
            return

        if event.key == pygame.K_RETURN:
            self.confirmed = True         
        elif event.key == pygame.K_ESCAPE:
            self.cancelled = True
            self.reset()
        elif event.key == pygame.K_BACKSPACE:
            self.buffer = self.buffer[:-1]
        elif event.unicode and event.unicode.isprintable():
            self.buffer += event.unicode

   
    def draw_preview(self, screen, color):
        
        if not self.active:
            return
        preview = self.font.render(self.buffer + "|", True, color)
        screen.blit(preview, self.pos)

    def commit(self, surface, color):
       
        if self.buffer:
            rendered = self.font.render(self.buffer, True, color)
            surface.blit(rendered, self.pos)
