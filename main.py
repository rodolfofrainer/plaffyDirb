import random
import os

import pygame

from classes import PlayerClass, PipeClass

# CONSTANTS
SCREEN_SIZE = (750, 1000)
FPS = 144
GRAVITY = 3
PLAYER_MAX_SPEED = 20


pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE))
clock = pygame.time.Clock()
running = True

player_image = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "plaffyDirb.png")))
player = PlayerClass(SCREEN_SIZE[0] / 8, SCREEN_SIZE[1] / 2, 30, player_image)
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


def frame_draw():
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


def instances_update():
    player.y += GRAVITY
    for pipe in pipes:
        pipe.x -= 2


def can_player_jump():
    if keys[pygame.K_SPACE]:
        player.y -= 6


def collision_detection(player, pipes):
    player_mask = pygame.mask.from_surface(player.image.convert_alpha())
    for pipe in pipes:
        pipe_mask = pygame.mask.from_surface(pipe.image)

        if pipe_mask.overlap(player_mask, (player.x-pipe.x, player.y-pipe.y)):
            pass  # handle collision detection


frame_interation = FPS
while running:
    frame_interation += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
            pygame.quit()
            quit()

    if player.y > (0+player.radius/2):
        can_player_jump()
    if player.y >= SCREEN_SIZE[1]:
        break

    for pipe in pipes:
        if pipe.x <= 0:
            pipes.remove(pipe)

    # spawn pipe on intervals
    spawn_pipe(frame_interation, 2)
    # Update instances positions
    instances_update()
    # draw the frame
    frame_draw()

    # detects if player mask and pipe mask collide
    collision_detection(player, pipes)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to constant
