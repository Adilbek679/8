import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Paint")

clock = pygame.time.Clock()
FPS = 60

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
active_color = COLORS["black"]
active_shape = 0  

panel_height = 100
button_size = 50
margin = 15

paintings = []

def draw_ui():
    """Рисует верхнюю панель с кнопками и цветами"""
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, panel_height))
    
    pygame.draw.rect(screen, HIGHLIGHT_COLOR if active_shape == 0 else (80,80,80), (margin, margin, button_size, button_size))
    pygame.draw.rect(screen, (230, 230, 230), (margin+10, margin+10, button_size-20, button_size-20))  # квадрат
    pygame.draw.rect(screen, HIGHLIGHT_COLOR if active_shape == 1 else (80,80,80), (margin*2+button_size, margin, button_size, button_size))
    pygame.draw.circle(screen, (230, 230, 230), (margin*2+button_size+button_size//2, margin+button_size//2), button_size//2-10)
    
    i = 0
    for name, color in COLORS.items():
        x = WIDTH - (len(COLORS)-i)*(button_size+margin)
        pygame.draw.rect(screen, color, (x, margin, button_size, button_size))
        if active_color == color:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (x-3, margin-3, button_size+6, button_size+6), 3)
        i += 1

def draw_paintings():
    """Рисует все сохраненные рисунки"""
    for paint in paintings:
        color, pos, shape = paint
        if shape == 0:
            pygame.draw.rect(screen, color, (pos[0]-15, pos[1]-15, 30, 30))
        elif shape == 1:
            pygame.draw.circle(screen, color, pos, 15)

def draw_current(mouse_pos):
    """Рисует текущий элемент, если мышь за пределами панели"""
    if mouse_pos[1] > panel_height:
        if active_shape == 0:
            pygame.draw.rect(screen, active_color, (mouse_pos[0]-15, mouse_pos[1]-15, 30, 30))
        else:
            pygame.draw.circle(screen, active_color, mouse_pos, 15)

running = True
while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    screen.fill(BACKGROUND_COLOR)
    draw_ui()
    draw_paintings()
    draw_current(mouse_pos)

    if mouse_click and mouse_pos[1] > panel_height:
        paintings.append((active_color, mouse_pos, active_shape))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paintings = []
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(margin, margin, button_size, button_size).collidepoint(event.pos):
                active_shape = 0
            elif pygame.Rect(margin*2+button_size, margin, button_size, button_size).collidepoint(event.pos):
                active_shape = 1
            i = 0
            for name, color in COLORS.items():
                x = WIDTH - (len(COLORS)-i)*(button_size+margin)
                if pygame.Rect(x, margin, button_size, button_size).collidepoint(event.pos):
                    active_color = color
                i += 1

    pygame.display.flip()

pygame.quit()
