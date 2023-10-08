from classes import PlayerClass, PipeClass
import random
import os

import pygame
import neat
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
pipes = [PipeClass(SCREEN_SIZE[0],
                   random.randint(
    player.radius*3, SCREEN_SIZE[1]-player.radius*2),
    50,
    SCREEN_SIZE[1],
    pygame.image.load(os.path.join("images", "PipeImage.png"))),
    PipeClass(SCREEN_SIZE[0],
              random.randint(
        player.radius*3, SCREEN_SIZE[1]-player.radius*2)-SCREEN_SIZE[1]-(player.radius*10),
    50,
    SCREEN_SIZE[1],
    pygame.transform.flip(pygame.image.load(os.path.join("images", "PipeImage.png")), False, True))]


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
        "Score: " + str(int(player.score/2)), 1, (255, 255, 255))
    screen.blit(
        score_label, (SCREEN_SIZE[0] - score_label.get_width() - 15, 10))


# update instances
def instances_update():
    player.y += GRAVITY
    for pipe in pipes:
        pipe.x -= 2

# Avaliate if a player can jump


def can_player_jump(keys):
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


def game_over():
    global running
    running = False


################### GAME ####################
def eval_genomes(genomes, config):
    global player
    global running
    frame_interation = FPS

    # NEAT
    nets = []
    ge = []
    players = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        # Create a new player instance for each genome
        player = PlayerClass(SCREEN_SIZE[0] / 8, SCREEN_SIZE[1] / 2, 30, player_image)
        players.append(player)

        ge.append(genome)

    while running and len(players) > 0:
        frame_interation += 1
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                game_over()

        # give each bird a fitness of 0.1 for each frame it stays alive
        for x, player in enumerate(players):
            ge[x].fitness += 0.1

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[players.index(player)].activate(
                (player.y, abs(player.y - pipes[0].x), abs(player.y - pipes[0].y)))
            print(output)
            # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            if output[0] > 0.5:
                player.jump()

            if player.y > (0+player.radius/2):
                player.y = (0+(player.radius))

            for pipe in pipes:
                if round(player.x) == round(pipe.x):
                    player.score += 1
                    for genome in ge:
                        genome.fitness += 5

            if player.y+player.image.get_height()/20 >= SCREEN_SIZE[1]:
                ge[players.index(player)].fitness -= 1
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))

        # detects if player can perform jump
        if player.y > (0+player.radius/2):
            can_player_jump(keys)

        for pipe in pipes:
            if pipe.x <= 0 - pipe.image.get_width():
                pipes.remove(pipe)
        # detects if player mask and pipe mask collide
        collision_detection(player, pipes)
        # Update instances positions
        instances_update()
        for player in players:
            # draw the frame
            frame_draw(player.score)

        # spawn pipe on intervals
        spawn_pipe(frame_interation, 2)
        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(FPS)  # limits FPS to constant
    pygame.quit()
    quit()


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
