import pygame
import sys
import math

pygame.init()


# Screen setup
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Paint")

clock = pygame.time.Clock()
FPS = 60

# Colors
BACKGROUND_COLOR = (30, 30, 30)
PANEL_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (200, 200, 200)
COLORS = {
    "blue": (0, 120, 255),
    "red": (255, 50, 50),
    "green": (50, 255, 100),
    "yellow": (255, 255, 50),
    "black": (0, 0, 0),
    "purple": (200, 50, 255),
    "eraser": BACKGROUND_COLOR 
}

active_shape = 0
active_color = COLORS["black"]

panel_height = 100
button_size = 50
margin = 15

paintings = []

drawing = False
start_pos = None

# Make sure coordinates are within canvas boundaries
def clamp_to_canvas(pos):
    x = max(0, min(WIDTH, pos[0]))
    y = max(panel_height, min(HEIGHT, pos[1]))
    return (x, y)

# Get rectangle from two points
def get_rect_from_points(p1, p2):
    p1 = clamp_to_canvas(p1)
    p2 = clamp_to_canvas(p2)
    x1, y1 = p1
    x2, y2 = p2
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return pygame.Rect(left, top, width, height)

# Draw square shape
def draw_square(surface, color, start, end, width=0):
    start = clamp_to_canvas(start)
    end = clamp_to_canvas(end)
    size = max(abs(end[0]-start[0]), abs(end[1]-start[1]))
    rect = pygame.Rect(start[0], start[1], size, size)
    if end[0] < start[0]: rect.x -= size
    if end[1] < start[1]: rect.y -= size
    rect.x = max(0, min(WIDTH - rect.width, rect.x))
    rect.y = max(panel_height, min(HEIGHT - rect.height, rect.y))
    pygame.draw.rect(surface, color, rect, width)

# Draw circle but stay within canvas
def draw_circle_clamped(surface, color, start, end, width=0):
    start = clamp_to_canvas(start)
    end = clamp_to_canvas(end)
    center = ((start[0]+end[0])//2, (start[1]+end[1])//2)
    radius = min(abs(end[0]-start[0])//2, abs(end[1]-start[1])//2)
    max_radius_x = min(center[0], WIDTH - center[0])
    max_radius_y = min(center[1]-panel_height, HEIGHT - center[1])
    radius = min(radius, max_radius_x, max_radius_y)
    pygame.draw.circle(surface, color, center, radius, width)

# Draw equilateral triangle
def draw_equilateral_triangle(surface, color, start, end, width=0):
    start = clamp_to_canvas(start)
    end = clamp_to_canvas(end)
    base = end[0] - start[0]
    height = abs(base) * math.sqrt(3)/2
    if end[1] < start[1]:
        height = -height
    point1 = start
    point2 = (start[0]+base, start[1])
    point3 = (start[0]+base/2, start[1]+height)
    points = [clamp_to_canvas(point1), clamp_to_canvas(point2), clamp_to_canvas(point3)]
    pygame.draw.polygon(surface, color, points, width)

# Draw rhombus
def draw_rhombus(surface, color, start, end, width=0):
    start = clamp_to_canvas(start)
    end = clamp_to_canvas(end)
    cx = (start[0]+end[0])//2
    cy = (start[1]+end[1])//2
    dx = abs(end[0]-start[0])//2
    dy = abs(end[1]-start[1])//2
    points = [(cx, start[1]), (end[0], cy), (cx, end[1]), (start[0], cy)]
    points = [clamp_to_canvas(p) for p in points]
    pygame.draw.polygon(surface, color, points, width)

# Draw right triangle
def draw_right_triangle(surface, color, start, end, width=0):
    start = clamp_to_canvas(start)
    end = clamp_to_canvas(end)

    x1, y1 = start
    x2, y2 = end

    p1 = (x1, y1)       
    p2 = (x2, y1)      
    p3 = (x1, y2)       

    points = [clamp_to_canvas(p1), clamp_to_canvas(p2), clamp_to_canvas(p3)]
    pygame.draw.polygon(surface, color, points, width)


# Draw top panel UI with shape icons and color buttons
def draw_ui(mouse_down=False):
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, panel_height))
    shapes_funcs = [draw_rect_icon, draw_circle_icon, draw_square_icon,
                    draw_triangle_icon, draw_rhombus_icon, draw_brush_icon,
                    draw_right_triangle_icon]

    for i, func in enumerate(shapes_funcs):
        x = margin + i*(button_size+margin)
        color_bg = HIGHLIGHT_COLOR if active_shape == i and (i != 5 or mouse_down) else (80,80,80)
        pygame.draw.rect(screen, color_bg, (x, margin, button_size, button_size))
        func(x, margin)

    # Draw color buttons
    for i, (name, color) in enumerate(COLORS.items()):
        x = WIDTH - (len(COLORS)-i)*(button_size+margin)
        pygame.draw.rect(screen, color, (x, margin, button_size, button_size))
        if active_color == color:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (x-3, margin-3, button_size+6, button_size+6), 3)

# Icons for shapes
def draw_rect_icon(x, y):
    pygame.draw.rect(screen, (230,230,230), (x+10, y+10, 30, 30), 2)
def draw_circle_icon(x, y):
    pygame.draw.circle(screen, (230,230,230), (x+25, y+25), 15, 2)
def draw_square_icon(x, y):
    pygame.draw.rect(screen, (230,230,230), (x+7, y+7, 36, 36), 2)
def draw_triangle_icon(x, y):
    points = [(x+10,y+40),(x+40,y+40),(x+25,y+10)]
    pygame.draw.polygon(screen, (230,230,230), points, 2)
def draw_rhombus_icon(x, y):
    points = [(x+25,y+10),(x+40,y+25),(x+25,y+40),(x+10,y+25)]
    pygame.draw.polygon(screen, (230,230,230), points, 2)
def draw_brush_icon(x, y):
    pygame.draw.line(screen, (230,230,230), (x+10, y+35), (x+40, y+15), 3)
def draw_right_triangle_icon(x, y):
    points = [(x+10, y+40), (x+40, y+40), (x+10, y+10)]
    pygame.draw.polygon(screen, (230,230,230), points, 2)

# Draw all saved paintings
def draw_paintings():
    for paint in paintings:
        color, start, end, shape = paint
        if shape == 0:
            pygame.draw.rect(screen, color, get_rect_from_points(start, end))
        elif shape == 1:
            draw_circle_clamped(screen, color, start, end)
        elif shape == 2:
            draw_square(screen, color, start, end)
        elif shape == 3:
            draw_equilateral_triangle(screen, color, start, end)
        elif shape == 4:
            draw_rhombus(screen, color, start, end)
        elif shape == 5:
            pygame.draw.line(screen, color, start, end, 5)
        elif shape == 6:
            draw_right_triangle(screen, color, start, end)


# Draw the current shape being drawn
def draw_current(start, end):
    if start and end and start[1] > panel_height and end[1] > panel_height:
        draw_paintings_helper(active_shape, active_color, start, end)

def draw_paintings_helper(shape, color, start, end):
    if shape == 0:
        pygame.draw.rect(screen, color, get_rect_from_points(start, end))
    elif shape == 1:
        draw_circle_clamped(screen, color, start, end)
    elif shape == 2:
        draw_square(screen, color, start, end)
    elif shape == 3:
        draw_equilateral_triangle(screen, color, start, end)
    elif shape == 4:
        draw_rhombus(screen, color, start, end)
    elif shape == 5:
        pygame.draw.line(screen, color, start, end, 5)
    elif shape == 6:
        draw_right_triangle(screen, color, start, end)


running = True
while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    screen.fill(BACKGROUND_COLOR)
    draw_ui(mouse_down=drawing and active_shape==5)
    draw_paintings()
    if drawing and active_shape != 5:
        draw_current(start_pos, mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            shapes_rects = [pygame.Rect(margin + i*(button_size+margin), margin, button_size, button_size) for i in range(7)]
            for i, rect in enumerate(shapes_rects):
                if rect.collidepoint(event.pos):
                    active_shape = i
            for i, (name, color) in enumerate(COLORS.items()):
                x = WIDTH - (len(COLORS)-i)*(button_size+margin)
                rect = pygame.Rect(x, margin, button_size, button_size)
                if rect.collidepoint(event.pos):
                    active_color = color
            if mouse_pos[1] > panel_height:
                drawing = True
                start_pos = mouse_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = clamp_to_canvas(event.pos)
                paintings.append((active_color, start_pos, end_pos, active_shape))
                drawing = False
                start_pos = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paintings = []

    # Draw brush continuously while holding mouse
    if drawing and active_shape == 5 and mouse_click and start_pos:
        sx, sy = start_pos
        sx = max(sx, 0)
        sy = max(sy, panel_height) 
        ex, ey = mouse_pos
        ex = max(ex, 0)
        ey = max(ey, panel_height) 
        paintings.append((active_color, (sx, sy), (ex, ey), 5))
        start_pos = (ex, ey)
    pygame.display.flip()

pygame.quit()
