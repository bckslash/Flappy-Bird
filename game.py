import pygame
import random
import time
import os
import math

WIDTH, HEIGHT = 500, 700
FPS = 60

VELOCITY = 8
PIPE_VELOCITY = 5
GRAVITY = 0.6
SPAWN_DELAY = 85
ANIMATION_DELAY = 10
HOLE = 25  # -160 full closed

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# sprites
BIRD = [pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprites', 'yellowbird-downflap.png')), (68, 48)),
        pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprites', 'yellowbird-midflap.png')), (68, 48)), 
        pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprites', 'yellowbird-upflap.png')), (68, 48))
]
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'sprites', 'background-day.png')), (WIDTH, HEIGHT))
PIPE_up = pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load(
    os.path.join('assets', 'sprites', 'pipe-green.png')).convert_alpha()), 0)
PIPE_down = pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load(
    os.path.join('assets', 'sprites', 'pipe-green.png')).convert_alpha()), 180)
FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'sprites', 'base.png')).convert_alpha())

def create_pipe(pipes):
        offset = random.randint(-180, 160)

        pipe = [pygame.Rect(((-HEIGHT-(HOLE)+PIPE_up.get_height()//2) + offset), WIDTH, PIPE_up.get_width(), PIPE_up.get_height(
        )), pygame.Rect(((HEIGHT+(HOLE)-PIPE_down.get_height()//2) + offset), WIDTH, PIPE_down.get_width(), PIPE_down.get_height())]

        pipes.append(pipe)

def move_pipes(pipes, bird):
    for pipe in pipes:
        pipe[0].y -= PIPE_VELOCITY
        pipe[1].y -= PIPE_VELOCITY
        
        if pipe[0].y + PIPE_up.get_width() < 0 and len(pipes) == 2:
            pipes.remove(pipe)

def create_floor(floors):
    ground = pygame.Rect(WIDTH, HEIGHT-BG.get_height()//6,
                         FLOOR.get_width(), FLOOR.get_height())

    floors.append(ground)

def move_floor(floors):
    for ground in floors:
        ground.x -= PIPE_VELOCITY

        if ground.y + FLOOR.get_width() < 0:
            floors.remove(ground)

def collide(bird, pipes):
    for pipe in pipes:
        offset_x = bird.x - pipe[0].x or bird.x - pipe[1].x
        offset_y = bird.y - pipe[0].y or bird.y - pipe[1].y
        return pipe.mask.overlap(bird.mask, (offset_x, offset_y)) != None

def game():
    clock = pygame.time.Clock()
    Run = True

    pipes = []
    floors = []
    bird_movement = 0
    wait_for_pipe = SPAWN_DELAY
    bird_state = 0
    delay = ANIMATION_DELAY
    score = 0

    bird = pygame.Rect(50, 50, BIRD[0].get_width(), BIRD[0].get_height())

    def draw_game():
        WIN.fill(BLACK)
        WIN.blit(BG, ((WIDTH//2)-(BG.get_width()//2), (HEIGHT//2)-(BG.get_height()//2)))
        
        for pipe in pipes:
            WIN.blit(PIPE_down, (pipe[0].y, pipe[0].x))
            WIN.blit(PIPE_up, (pipe[1].y, pipe[1].x))

        WIN.blit(BIRD[bird_state], (bird.y, bird.x))

        for ground in floors:
            WIN.blit(FLOOR, (ground.x, ground.y))
            
        # WIN.blit(FLOOR, (0, HEIGHT-BG.get_height()//6))
        pygame.display.update()

    while Run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed() 

        if keys_pressed[pygame.K_SPACE] and bird.x > BIRD[0].get_height():
            bird_movement = 0
            bird_movement -= VELOCITY

            if bird_state == 1: bird_state += 1
            if bird_state >= 3: bird_state = 0

        for pipe in pipes:
            if bird.colliderect(pipe[0]):
                print(1)
            if bird.colliderect(pipe[1]):
                print(2)

        if bird.x + BIRD[0].get_height() < HEIGHT-BG.get_height()//6:  # floor
            bird_movement += GRAVITY
            bird.x += int(bird_movement)
        else:
            time.sleep(0.5)
            Run = False

        wait_for_pipe -= 1
        if wait_for_pipe <= 0:
            create_pipe(pipes)
            create_floor(floors)
            wait_for_pipe = SPAWN_DELAY
        move_pipes(pipes, bird)
        move_floor(floors)

        delay -= 1
        if delay <= 0:
            bird_state += 1
            if bird_state >= 3:
                bird_state = 0
            delay = ANIMATION_DELAY

        for pipe in pipes:
            if bird.colliderect(pipe[0]) or bird.colliderect(pipe[1]):
                print(1)
        

        draw_game()

    pygame.quit()

if __name__ == "__main__":
    game()
