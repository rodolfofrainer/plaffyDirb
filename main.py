from classes import PlayerClass, PipeClass
import random
import os

import pygame
pygame.font.init()


# CONSTANTS
SCREEN_SIZE = (750, 1000)
FPS = 144
GRAVITY = 3
PLAYER_MAX_SPEED = 20
STAT_FONT = pygame.font.SysFont("comicsans", 50)

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE))
clock = pygame.time.Clock()
running = True


# PLAYER
player_image = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "plaffyDirb.png")))
player = PlayerClass(SCREEN_SIZE[0] / 8, SCREEN_SIZE[1] / 2, 30, player_image)

# PIPES
pipes = []


def spawn_pipe(frame_interation, frequency):
    if frame_interation % (FPS * frequency) == 0:
        pipe_x = SCREEN_SIZE[0]
        pipe_y = random.randint(
            player.radius*3, SCREEN_SIZE[1]-player.radius*2)
        pipe_length = SCREEN_SIZE[1]
        pipe_width = 50
        pipe_image = pygame.image.load(os.path.join("images", "PipeImage.png"))

        pipe = PipeClass(pipe_x,
                         pipe_y,
                         pipe_width,
                         pipe_length,
                         pipe_image)
        pipes.append(pipe)
        pipe2 = PipeClass(pipe_x,
                          pipe_y-pipe_length-(player.radius*10),
                          pipe_width,
                          pipe_length,
                          pygame.transform.flip(pipe_image, False, True))
        pipes.append(pipe2)

# Draw screen


def frame_draw(score):
    PLAYER_POSITION = (player.x-player.image.get_width()/2,
                       player.y-player.image.get_height()/2)

    screen.fill("blue")
    screen.blit(player.image, PLAYER_POSITION)

    for pipe in pipes:
        screen.blit(pipe.image, (pipe.x, pipe.y))
    if len(pipes) > 0:
        if pipes[0].x > player.x:
            pygame.draw.line(screen,
                             pygame.Color("white"),
                             ((PLAYER_POSITION[0]+player.image.get_width()),
                              (PLAYER_POSITION[1]+player.image.get_width()/2)),
                             (pipes[0].x+pipes[0].image.get_width()/2,
                              pipes[0].y))
            pygame.draw.line(screen,
                             pygame.Color("white"),
                             ((PLAYER_POSITION[0]+player.image.get_width()),
                              (PLAYER_POSITION[1]+player.image.get_width()/2)),
                             (pipes[1].x+pipes[1].image.get_width()/2,
                              pipes[1].y+pipes[1].image.get_height()))
        else:
            pygame.draw.line(screen,
                             pygame.Color("white"),
                             ((PLAYER_POSITION[0]+player.image.get_width()),
                              (PLAYER_POSITION[1]+player.image.get_width()/2)),
                             (pipes[-2].x+pipes[-2].image.get_width()/2,
                              pipes[-2].y))
            pygame.draw.line(screen,
                             pygame.Color("white"),
                             ((PLAYER_POSITION[0]+player.image.get_width()),
                              (PLAYER_POSITION[1]+player.image.get_width()/2)),
                             (pipes[-1].x+pipes[-1].image.get_width()/2,
                              pipes[-1].y+pipes[-1].image.get_height()))

    # render score
    score_label = STAT_FONT.render(
        "Score: " + str(int(score)), 1, (255, 255, 255))
    screen.blit(
        score_label, (SCREEN_SIZE[0] - score_label.get_width() - 15, 10))


# update instances
def instances_update():
    player.y += GRAVITY
    for pipe in pipes:
        pipe.x -= 2

# Avaliate if a player can jump
def can_player_jump():
    if player.y > (0+player.radius/2):
        if keys[pygame.K_SPACE]:
            player.jump()


# detect if player and pipes colided
def collision_detection(player, pipes):
    player_mask = pygame.mask.from_surface(player.image)
    for pipe in pipes:
        pipe_mask = pygame.mask.from_surface(pipe.image)
        if pipe_mask.overlap(player_mask, (player.x-player.radius-pipe.x, player.y-player.radius-pipe.y)):
            game_over()
            pass  # need to handle collision for AI

# Breaks game loop and finish program
def game_over(running=False):
    running = False
    pygame.quit()
    quit()


################### GAME ####################
frame_interation = FPS
score = 0
while running:
    frame_interation += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            game_over()
    if player.y+player.image.get_height()/20 >= SCREEN_SIZE[1]:
        game_over()

    can_player_jump()

    for pipe in pipes:
        if round(player.x) == round(pipe.x):
            score += 0.5

        if pipe.x <= 0 - pipe.image.get_width():
            pipes.remove(pipe)

    # spawn pipe on intervals
    spawn_pipe(frame_interation, 2)
    # Update instances positions
    instances_update()
    # draw the frame
    frame_draw(score)

    # detects if player mask and pipe mask collide
    collision_detection(player, pipes)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to constant
