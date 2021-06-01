import pygame
import sys
import random
import os
import math

def draw_floor():
    screen.blit(FLOOR, (floor_x_pos, HEIGHT - FLOOR.get_height()+30))
    screen.blit(FLOOR, (floor_x_pos + WIDTH,
                HEIGHT - FLOOR.get_height()+30))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = PIPE.get_rect(midtop=(HEIGHT, random_pipe_pos))
    top_pipe = PIPE.get_rect(midbottom=(HEIGHT, random_pipe_pos-180))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= VELOCITY
	return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= WIDTH:
            screen.blit(PIPE, pipe)
        else:
            flip_pipe = pygame.transform.flip(PIPE, False, True)
            screen.blit(flip_pipe, pipe)

def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx == -30:
            pipes.remove(pipe)
    return pipes

def check_collision(pipes):
    global deaths
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            deaths += 1
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= HEIGHT-20:
        return False

    return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
	return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH//2, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(WIDTH//2, 565))
        screen.blit(high_score_surface, high_score_rect)

        deaths_surface = game_font.render(
            f'Deaths: {int(deaths)}', True, (255, 255, 255))
        deaths_rect = deaths_surface.get_rect(center=(WIDTH//2, HEIGHT-deaths_surface.get_height()-10))
        screen.blit(deaths_surface, deaths_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
        with open("score.txt", "w") as f:
            f.write(str(math.ceil(high_score)))
    return high_score

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
WIDTH, HEIGHT = 450, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font(os.path.join('assets', '04B_19.TTF'), 45)

# Game Variables
FPS = 120
GRAVITY = 0.30
VELOCITY = 2
PIPE_SPAWN = 1500
score = 0
high_score = 0
deaths = 0
with open("score.txt", "r") as f:
    high_score = float(f.read())

bird_movement = 0
game_active = False

BG = pygame.image.load(os.path.join('assets', 'sprites', 'background-day.png')).convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

FLOOR = pygame.image.load(os.path.join(
	'assets', 'sprites', 'base.png')).convert()
FLOOR = pygame.transform.scale(FLOOR, (WIDTH, 112))
floor_x_pos = 0

BIRD_DOWN = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'sprites', 'redbird-downflap.png')), (54, 34)).convert_alpha()
BIRD_MID = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'sprites', 'redbird-midflap.png')), (54, 34)).convert_alpha()
BIRD_UP = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'sprites', 'redbird-upflap.png')), (54, 34)).convert_alpha()
bird_frames = [BIRD_DOWN, BIRD_MID, BIRD_UP]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 200))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

PIPE = pygame.image.load(os.path.join(
    'assets', 'sprites', 'pipe-green.png'))
PIPE = pygame.transform.scale(PIPE, (82, 350))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, PIPE_SPAWN)
pipe_height = [270, 300, 330, 360, 390, 420, 450, 480, 520]

GAME_OVER = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'sprites', 'message.png')), (WIDTH//2+20, HEIGHT//2)).convert_alpha()
game_over_rect = GAME_OVER.get_rect(center=(WIDTH//2, 300))

flap_sound = pygame.mixer.Sound(os.path.join(
    'assets', 'audio', 'wing.wav'))
death_sound = pygame.mixer.Sound(os.path.join(
    'assets', 'audio', 'hit.wav'))
score_sound = pygame.mixer.Sound(os.path.join(
    'assets', 'audio', 'point.wav'))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 200)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(BG, (0, 0))

    if game_active:
        # Bird
        bird_movement += GRAVITY
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipes(pipe_list)


        draw_floor()
        score_display('main_game')
        for pipe in pipe_list:
            if pipe.centerx == 100:
                score += 0.5
                if not float(score).is_integer():
                    score_sound.play()
    else:
        screen.blit(GAME_OVER, game_over_rect)
        high_score = update_score(score, high_score)
        score = 0
        score_display('game_over')

    # Floor
    floor_x_pos -= VELOCITY
    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(FPS)
