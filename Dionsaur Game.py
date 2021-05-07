import pygame
import os 
import random

pygame.init()

pygame.display.set_caption("First Game")

screen_H = 700
screen_W = 500

#assets
canvas = pygame.display.set_mode((screen_H,screen_W))

RUNNING = [pygame.image.load(os.path.join("Assets\Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets\Dino", "DinoRun2.png"))]

DUCK = [pygame.image.load(os.path.join("Assets\Dino", "DinoDuck1.png")),
       pygame.image.load(os.path.join("Assets\Dino", "DinoDuck2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets\Other", "Cloud.png"))

OBSTACLE_SMALL = [pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus1.png")),
                  pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus2.png")),
                  pygame.image.load(os.path.join("Assets\Cactus", "SmallCactus3.png"))]

OBSTACLE_LARGE = [pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus1.png")),
                  pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus2.png")),
                  pygame.image.load(os.path.join("Assets\Cactus", "LargeCactus3.png"))]

ROAD = pygame.image.load(os.path.join("Assets\Other", "Track.png"))

START = pygame.image.load(os.path.join("Assets\Other","Start.png"))
EXIT = pygame.image.load(os.path.join("Assets\Other","exit.png"))
RESET = pygame.image.load(os.path.join("Assets\Other","Reset.png"))
GAME_OVER = pygame.image.load(os.path.join("Assets\Other","GameOver.png"))

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
        global game_speed
        self.image = self.run_img[self.step_index  // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = player.pos_x
        self.dino_rect.y = player.pos_y
        self.step_index += int(game_speed/10)
        
    def jump_act(self):
        if self.jump: 
            self.dino_rect.y -= self.jump_vel * 5
            self.jump_vel -= 0.6
        if self.jump_vel < - self.do_jump:
            self.jump = False
            self.jump_vel = self.do_jump

    def duck_act(self):
        global game_speed
        self.image = self.duck_img[self.step_index //5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = player.pos_x
        self.dino_rect.y = player.pos_y + self.do_duck
        self.step_index +=  int(game_speed/10)

    def draw(self, canvas):
        canvas.blit(self.image, self.dino_rect)

class score:
    def __init__(self):
        self.points = -1
        self.count = 0
        self.font = pygame.font.Font('freesansbold.ttf',20)

    def nambah(self):
        if(self.count % 5 == 0 and self.count > 1):
            self.points += 11
        else :
            self.points +=1 
        if (self.count % 10 == 0 and self.count >= 1):
            global game_speed
            game_speed += 1
        self.count +=1      
    def tampilkan(self):
        
        text = self.font.render("Points : " + str(self.points),True,(0,0,0))
        textRect = text.get_rect() 
        textRect.center = (100 ,40)
        canvas.blit(text,textRect)      

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

class obstacle:
    def __init__(self,image,tipe):
        self.image = image
        self.type = tipe
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_W * 2

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            rintangan.pop()

    def draw(self, canvas):
        canvas.blit(self.image[self.type],self.rect)

class smallobstacle(obstacle):
    def __init__(self,image):
        self.type = random.randint(0,2)
        super().__init__(image,self.type)
        self.rect.y = 350

class Largeobstacle(obstacle):
    def __init__(self,image):
        self.type = random.randint(0,2)
        super().__init__(image,self.type)
        self.rect.y = 325

def start() : 
    run = True 
    
    trex = player()
    Cloud = cloud()
    Background = bg()
    skor = score()
    
    global game_speed,rintangan
    game_speed = 10
    rintangan = []

    while run :
        clock = pygame.time.Clock()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()

        canvas.fill((255,255,255))
        trex.draw(canvas)
        trex.update(keys)

        if len(rintangan) == 0:
            if random.randint(0,1) == 1 :
                rintangan.append(smallobstacle(OBSTACLE_SMALL))
                skor.nambah()
            elif random.randint(0,1) == 1:
                rintangan.append(Largeobstacle(OBSTACLE_LARGE))
                skor.nambah()

        for i in rintangan:
            i.draw(canvas)
            i.update()
            if trex.dino_rect.colliderect(i.rect):
                restart(skor.points)
        
        Background.update()
        Cloud.draw(canvas)
        Cloud.update()
        skor.tampilkan()

        clock.tick(30)
        pygame.display.update()

    pygame.quit()

def restart(skor):
    run = True
    while run :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    start()
                elif exit_rect.collidepoint(event.pos):
                    run = False

        canvas.fill((255,255,255))

        font = pygame.font.Font('freesansbold.ttf',20)
        if (skor < 5):
            text = font.render("Kamu Cupu poin kamu cuma : " + str(skor),True,(0,0,0))
        else :
            text = font.render("Kamu hebat banget poin kamu : " + str(skor),True,(0,0,0))
        textRect = text.get_rect() 
        textRect.center = (350 , 150)
        canvas.blit(text,textRect) 

        restart_rect = RESET.get_rect()
        restart_rect.x = 300
        restart_rect.y = 270

        exit_rect = EXIT.get_rect()
        exit_rect.x = 270
        exit_rect.y = 400
        canvas.blit(EXIT,exit_rect)

        canvas.blit(GAME_OVER,(170,200))
        canvas.blit(RESET,restart_rect)
        pygame.display.update()

    pygame.quit() 

def main_menu():
    run = True 
    while run :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    start()
                elif exit_rect.collidepoint(event.pos):
                    run = False

        canvas.fill((255,255,255))

        start_rect = START.get_rect()
        start_rect.x = 265
        start_rect.y = 150

        exit_rect = EXIT.get_rect()
        exit_rect.x = 265
        exit_rect.y = 250

        canvas.blit(START,start_rect)
        canvas.blit(EXIT,exit_rect)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__" :
    main_menu()
d