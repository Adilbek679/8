import pygame, sys, random
pygame.init()


screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Змейка")


background = pygame.transform.scale(pygame.image.load("images/back.png"), (800,800))

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


cell = 32
fps = 8
clock = pygame.time.Clock()

def reset_game():
    snake = [(100,100),(68,100),(36,100)]
    direction = "right"
    apple = spawn_apple()
    walls = spawn_walls(15)  # количество стен можно менять
    return snake, direction, apple, [], False, walls


def spawn_apple():
    return random.randint(2,24)*32, random.randint(2,24)*32
def spawn_walls(count=10):
    walls = set()
    while len(walls) < count:
        wx = random.randint(1, 23) * 32
        wy = random.randint(1, 23) * 32
        if (wx, wy) not in snake and (wx, wy) != (apple_x, apple_y):
            walls.add((wx, wy))
    return list(walls)

wall_img = pygame.transform.scale(pygame.image.load("images/wall.png"), (32,32))


snake, direction, (apple_x, apple_y), turns, game_over, walls = reset_game()

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

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if game_over and e.type == pygame.KEYDOWN:
            snake, direction, (apple_x, apple_y), turns, game_over = reset_game()

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

        # проверка на выход за пределы → смерть
    if nx < 0 or nx > 800-cell or ny < 0 or ny > 800-cell:
        game_over = True



    snake.insert(0,(nx,ny))
            # столкновение со стеной
    if (nx,ny) in walls:
        game_over = True


        # check apple
        if pygame.Rect(nx,ny,32,32).colliderect(pygame.Rect(apple_x,apple_y,50,50)):
            apple_x, apple_y = spawn_apple()
        else:
            snake.pop()

        # self collision
        if snake[0] in snake[1:]:
            game_over = True

    screen.blit(background,(0,0))

    if game_over:
        text = font.render("GAME OVER", True, (255,0,0))
        restart = font.render("Press any key", True, (255,255,255))
        screen.blit(text,(250,350))
        screen.blit(restart,(220,420))
        pygame.display.update()
        clock.tick(fps)
        continue
    

    # --- DRAW SNAKE ---
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
    for wx, wy in walls:
    screen.blit(wall_img, (wx, wy))

    screen.blit(apple,(apple_x,apple_y))
    pygame.display.update()
    clock.tick(fps)
