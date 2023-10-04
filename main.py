import random
import os

import pygame

from classes import PlayerClass, PipeClass

# CONSTANTS
SCREEN_SIZE = (750, 1000)
FPS = 144
GRAVITY = 5
PLAYER_MAX_SPEED = 20
PIPE_SPAWN_RATE = 2 * FPS


pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE))
clock = pygame.time.Clock()
running = True

player_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "plaffyDirb.png")))
player = PlayerClass(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2, 30, player_image)
pipes = []


def spawn_pipe(frame_interation):
    if frame_interation % PIPE_SPAWN_RATE == 0:
        pipe_x = SCREEN_SIZE[0]
        pipe_y = random.randint(
            player.radius*2, SCREEN_SIZE[1]-player.radius*2)
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
                          pipe_y-pipe_length-(player.radius*6),
                          pipe_width,
                          pipe_length,
                          pygame.transform.flip(pipe_image, False, True))
        pipes.append(pipe2)


def frame_draw():
    screen.fill("blue")
    screen.blit(player.image, (player.x,player.y))
    for pipe in pipes:
        screen.blit(pipe.image,(pipe.x, pipe.y))


def instances_update():
    player.y += GRAVITY
    for pipe in pipes:
        pipe.x -= 2


def can_player_jump():
    if keys[pygame.K_SPACE]:
        player.y -= 10


def collision_detection(player, pipes):
    player_mask = pygame.mask.from_surface(player.image.convert_alpha())
    for pipe in pipes:
        pipe_mask = pygame.mask.from_surface(pipe.image)
        
        if pipe_mask.overlap(player_mask, (player.x-pipe.x,player.y-pipe.y)):
            print("collision")

        


frame_interation = PIPE_SPAWN_RATE/3
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

    spawn_pipe(frame_interation)
    instances_update()
    frame_draw()

    collision_detection(player, pipes)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to constant
