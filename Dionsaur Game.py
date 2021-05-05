import pygame
import os 
import random

pygame.init()

pygame.display.set_caption("First Game")

screen_H = 700
screen_W = 500

canvas = pygame.display.set_mode((screen_H,screen_W))

RUNNING = [pygame.image.load(os.path.join("Assets\Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets\Dino", "DinoRun2.png"))]

DUCK = [pygame.image.load(os.path.join("Assets\Dino", "DinoDuck1.png")),
       pygame.image.load(os.path.join("Assets\Dino", "DinoDuck2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets\Other", "Cloud.png"))

ROAD = pygame.image.load(os.path.join("Assets\Other", "Track.png"))

class player:
    pos_x = 15
    pos_y = 330

    def __init__(self):
        #image
        self.run_img = RUNNING
        self.duck_img = DUCK

        self.jump = False 
        self.run = True
        self.duck = False

        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.do_duck = 30
        self.do_jump = 8.5
        self.jump_vel = 8.5

        self.dino_rect.x = player.pos_x
        self.dino_rect.y = player.pos_y

    def update(self, keys):
        if self.run:
            self.run_act()
        if self.jump:
            self.jump_act()
        if self.duck:
            self.duck_act()
            
        if self.step_index >= 10:
            self.step_index = 0

        if keys[pygame.K_SPACE] and not self.jump :
            self.run = False
            self.jump = True
            self.duck =  False
        elif keys[pygame.K_DOWN] and not self.jump :
            self.run = False
            self.jump = False
            self.duck = True
        elif not self.jump or self.duck :
            self.run = True
            self.jump = False
            self.duck = False

    def run_act(self):
        self.image = self.run_img[self.step_index //5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = player.pos_x
        self.dino_rect.y = player.pos_y
        self.step_index += 1
        
    def jump_act(self):
        if self.jump: 
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.do_jump:
            self.jump = False
            self.jump_vel = self.do_jump

    def duck_act(self):
        self.image = self.duck_img[self.step_index //5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = player.pos_x
        self.dino_rect.y = player.pos_y + self.do_duck
        self.step_index += 1

    def draw(self, canvas):
        canvas.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class score:
    def __init__(self):
        self.score = 0

class cloud:
    def __init__(self):
        self.x = screen_H + random.randint(500,800)
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self):
        self.x -= game_speed
        if self.x < - self.width:
            self.x = screen_W + random.randint(2500,3000)
            self.y = random.randint(50,100)

    def draw(self, canvas):
        canvas.blit(self.image, (self.x,self.y))

class bg:
    bg_x = 0
    bg_y = 400
    def __init__(self):
        self.image_width = ROAD.get_width()

    def update(self):
        canvas.blit(ROAD, (bg.bg_x,bg.bg_y))
        canvas.blit(ROAD, (self.image_width + bg.bg_x, bg.bg_y))
        if bg.bg_x <= -self.image_width:
            canvas.blit(ROAD, (self.image_width + bg.bg_x,bg.bg_y))
            bg.bg_x = 0
        bg.bg_x -= game_speed
    
def start() : 
    run = True 

    trex = player()
    Cloud = cloud()
    Background = bg()

    global game_speed 
    game_speed = 10

    while run :
        clock = pygame.time.Clock()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()

        canvas.fill((255,255,255))
        trex.draw(canvas)
        trex.update(keys)

        Background.update()

        Cloud.draw(canvas)
        Cloud.update()

        clock.tick(30)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__" :
    start()