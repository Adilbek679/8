import pygame, sys
from pygame.locals import *
import random, time
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  
SCORE = 0  
COIN = 0 
 
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("images/AnimatedStreet.png")
background = pygame.transform.scale(background, (400, 600))
 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        # Load and scale enemy car
        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 90))
        self.rect = self.image.get_rect()
        # Spawn randomly at the top
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        # Enemy moves down
        self.rect.move_ip(0,SPEED)
        # When leaving the screen, respawn at top and increase score
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load and scale player car
        self.image = pygame.image.load("images/Player.png")
        self.image = pygame.transform.scale(self.image, (50, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Simple left-right movement 
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create first coin immediately
        self.new_coin() 

    def new_coin(self):
        # Randomly choose one of three coin types
        coin_number = random.randint(1, 3)

        if coin_number == 1:
            self.image = pygame.image.load("images/coin_50.png")
            self.image = pygame.transform.scale(self.image, (40, 40))
            self.value = 50

        elif coin_number == 2:
            self.image = pygame.image.load("images/coin_100.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.value = 100

        else:
            self.image = pygame.image.load("images/coin_200.png")
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.value = 200

        
        # Reset coin position at top
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

    def move(self):
        # Move coin downward
        self.rect.move_ip(0, 5)
         # If coin falls out, generate a new one
        if self.rect.top > SCREEN_HEIGHT:
            self.new_coin()

                   
P1 = Player()
E1 = Enemy()
C1 = Coin()
 
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
coins_group = pygame.sprite.Group()
coins_group.add(C1)
all_sprites.add(C1)

 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
while True:
       
    for event in pygame.event.get():   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    coins = font_small.render(str(COIN), True, BLACK)
    DISPLAYSURF.blit(coins,(350, 10))
 
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
        
    if pygame.sprite.spritecollideany(P1, coins_group):
        COIN += C1.value 
        pygame.mixer.Sound('images/coin.mp3').play()
        SPEED = COIN / 200 + 5
        C1.new_coin()  


    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('images/crash.mp3').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)