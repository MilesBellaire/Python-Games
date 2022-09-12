from time import time
from tracemalloc import start
import pygame
import numpy as np
import os
import random
import NN_API as ai

pygame.font.init()

WIDTH, HEIGHT = 500, 800
generation = 1
score = 0

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), 
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    GOAL = 40

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

        self.neural_network = ai.Neural_Network([3, 2, 1], ai.Activation_Inverse_Tan())
        self.score = 0
        self.alive = True

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16
        
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def change_WaB(self, score):
        max_range = 0.03
        print("goal:", self.GOAL)
        print("score:", score)
        if self.GOAL < score:
            r = 1/self.GOAL * max_range
        else: 
            r = (self.GOAL-score)/self.GOAL * max_range
        print(r)
        print()
        self.neural_network.shift_weights(r)

    def should_jump(self, topY, botY):
        self.neural_network.forward([self.y, topY, botY])
        return self.neural_network.YoN()
        

class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5
    width = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        bird.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    text2 = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text2, (10, 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()

def main():
    global score
    birds = []
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    num_birds = 30
    start_time = time()

    def reset():
        global score, start_time, generation

        # sort birds
        def func(b: Bird):
            return  b.score
        birds.sort(reverse=True, key=func)
        best_bird = birds[0]
        generation += 1

        birds.clear()
        for i in range(num_birds):
            new_bird = Bird(230, random.randrange(300, 400))
            new_bird.neural_network = best_bird.neural_network.clone()
            new_bird.change_WaB(best_bird.score)
            birds.append(new_bird)
        for bird in birds[0:3]:
            bird.score = 0
            birds.append(bird)

        pipes.clear()
        pipes.append(Pipe(600))
        score = 0
        start_time = time()

    for i in range(num_birds):
        birds.append(Bird(230, random.randrange(300, 400)))

    birds_alive = True
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        birds_alive = False
        for bird in birds:
            bird.move()

            if bird.alive:
                birds_alive = True
                bird.score = time()- start_time 
                cur_pipe = pipes[0]
                if bird.should_jump(cur_pipe.top+30, cur_pipe.bottom+30) and bird.y > 30:
                    bird.jump()
            else:
                bird.x -= 5

        if not birds_alive:
            reset()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for bird in birds:
                if pipe.collide(bird):
                    bird.alive = False
                    bird.vel = 0

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            if not pipe.passed and pipe.x < 220:
                pipe.passed = True
                add_pipe = True
            
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() >= 730:
                bird.alive = False

        base.move()
        draw_window(win, birds, pipes, base, score, generation)

    pygame.quit()
    quit()

main()