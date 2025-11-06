import pygame, sys, random
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Змейка")

background = pygame.transform.scale(pygame.image.load("images/back.png"), (800,800))
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("images/eatsound.mp3")

snake_imgs = {
    "head": {
        "up": pygame.transform.scale(pygame.image.load("images/snake/headu.png"), (50,50)),
        "right": pygame.transform.scale(pygame.image.load("images/snake/headr.png"), (50,50)),
        "down": pygame.transform.scale(pygame.image.load("images/snake/headd.png"), (50,50)),
        "left": pygame.transform.scale(pygame.image.load("images/snake/headl.png"), (50,50)),
    },
    "body_h": pygame.transform.scale(pygame.image.load("images/snake/body.png"), (32,32)),
    "body_v": pygame.transform.scale(pygame.image.load("images/snake/bodyver.png"), (32,32)),
    "turn": {
        "lu": pygame.transform.scale(pygame.image.load("images/snake/lu.png"), (32,32)),
        "ru": pygame.transform.scale(pygame.image.load("images/snake/ru.png"), (32,32)),
        "rd": pygame.transform.scale(pygame.image.load("images/snake/rd.png"), (32,32)),
        "ld": pygame.transform.scale(pygame.image.load("images/snake/ld.png"), (32,32)),
    },
    "tail": {
        "up": pygame.transform.scale(pygame.image.load("images/snake/tailu.png"), (32,32)),
        "right": pygame.transform.scale(pygame.image.load("images/snake/tailr.png"), (32,32)),
        "down": pygame.transform.scale(pygame.image.load("images/snake/taild.png"), (32,32)),
        "left": pygame.transform.scale(pygame.image.load("images/snake/taill.png"), (32,32)),
    }
}

apple = pygame.transform.scale(pygame.image.load("images/apple.png"), (50,50))

font = pygame.font.SysFont("Arial", 50, True)
small_font = pygame.font.SysFont("Arial", 30, True)

cell = 32
fps = 8
clock = pygame.time.Clock()

# ---- GAME RESET FUNCTION ----
def reset_game():
    snake = [(100,100),(68,100),(36,100)]
    direction = "right"
    apple_x, apple_y = spawn_apple(snake)
    turns = []
    game_over = False
    score = 0
    level = 1
    return snake, direction, apple_x, apple_y, turns, game_over, score, level

# ---- SPAWN APPLE NOT ON SNAKE ----
def spawn_apple(snake):
    while True:
        x = random.randint(2,24)*32
        y = random.randint(2,24)*32
        if (x,y) not in snake:
            return x,y

def next_pos(x,y,dir):
    if dir=="up": return (x, y-cell)
    if dir=="down": return (x, y+cell)
    if dir=="left": return (x-cell, y)
    if dir=="right": return (x+cell, y)

def get_corner(prev, cur, nxt):
    px,py = prev; cx,cy = cur; nx,ny = nxt
    dx1,dy1 = cx-px, cy-py
    dx2,dy2 = nx-cx, ny-cy

    if dx1 > 0 and dy2 < 0: return snake_imgs["turn"]["ru"]
    if dy1 < 0 and dx2 > 0: return snake_imgs["turn"]["rd"]
    if dx1 < 0 and dy2 > 0: return snake_imgs["turn"]["ld"]
    if dy1 > 0 and dx2 > 0: return snake_imgs["turn"]["lu"]
    if dx1 > 0 and dy2 > 0: return snake_imgs["turn"]["rd"]
    if dy1 > 0 and dx2 < 0: return snake_imgs["turn"]["ld"]
    if dx1 < 0 and dy2 < 0: return snake_imgs["turn"]["lu"]
    if dy1 < 0 and dx2 < 0: return snake_imgs["turn"]["ru"]
    return None

snake, direction, apple_x, apple_y, turns, game_over, score, level = reset_game()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if game_over and e.type == pygame.KEYDOWN:
            snake, direction, apple_x, apple_y, turns, game_over, score, level = reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        old = direction
        if keys[pygame.K_UP] and direction!="down": direction="up"
        elif keys[pygame.K_DOWN] and direction!="up": direction="down"
        elif keys[pygame.K_LEFT] and direction!="right": direction="left"
        elif keys[pygame.K_RIGHT] and direction!="left": direction="right"

        if old != direction:
            turns.append((snake[0][0], snake[0][1], direction))

        nx,ny = next_pos(*snake[0], direction)

        # ---- BORDER TELEPORT ----
        if nx < 0: nx = 800 - cell
        elif nx > 800 - cell: nx = 0
        if ny < 0: ny = 800 - cell
        elif ny > 800 - cell: ny = 0

        snake.insert(0,(nx,ny))

        # ---- EAT APPLE ----
        if pygame.Rect(nx,ny,32,32).colliderect(pygame.Rect(apple_x,apple_y,50,50)):
            score += 1
            eat_sound.play(maxtime=1200)


            # LEVEL UP EVERY 4 APPLES
            if score % 4 == 0:
                level += 1
                fps += 1  # increase speed

            apple_x, apple_y = spawn_apple(snake)
        else:
            snake.pop()

        # ---- SELF COLLISION ----
        if snake[0] in snake[1:]:
            game_over = True

    screen.blit(background,(0,0))

    # ---- DRAW GAME OVER ----
    if game_over:
        text = font.render("GAME OVER", True, (255,0,0))
        restart = font.render("Press any key", True, (255,255,255))
        screen.blit(text,(250,350))
        screen.blit(restart,(220,420))
        pygame.display.update()
        clock.tick(fps)
        continue

    # ---- DRAW SNAKE ----
    for i,(x,y) in enumerate(snake):
        if i==0:
            screen.blit(snake_imgs["head"][direction],(x,y))
        elif i==len(snake)-1:
            tx,ty = snake[-1]
            px,py = snake[-2]
            if tx<px: taildir="left"
            elif tx>px: taildir="right"
            elif ty<py: taildir="up"
            else: taildir="down"
            screen.blit(snake_imgs["tail"][taildir], (tx,ty))
        else:
            prev = snake[i+1]; nxt = snake[i-1]
            corner = get_corner(prev,(x,y),nxt)
            if corner: screen.blit(corner,(x,y))
            else:
                img = snake_imgs["body_v"] if prev[0]==nxt[0] else snake_imgs["body_h"]
                screen.blit(img,(x,y))

    # ---- DRAW APPLE ----
    screen.blit(apple,(apple_x,apple_y))

    # ---- DRAW SCORE & LEVEL ----
    score_text = small_font.render(f"Score: {score}", True, (255,255,255))
    level_text = small_font.render(f"Level: {level}", True, (255,255,0))
    screen.blit(score_text,(10,10))
    screen.blit(level_text,(10,40))

    pygame.display.update()
    clock.tick(fps)
