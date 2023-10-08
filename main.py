import os
import random
import pygame
import neat
from classes import PlayerClass, PipeClass  # Import your custom classes

# CONSTANTS
SCREEN_SIZE = (750, 1000)
FPS = 144
GRAVITY = 3

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# PLAYER
player_image = pygame.transform.scale2x(
    pygame.image.load(os.path.join("images", "plaffyDirb.png")))
player = PlayerClass(SCREEN_SIZE[0] / 8, SCREEN_SIZE[1] / 2, 30, player_image)

# PIPES
pipes = []

# Initialize NEAT variables
gen = 0

def spawn_pipe():
    pipe_x = SCREEN_SIZE[0]
    pipe_y = random.randint(player.radius * 3, SCREEN_SIZE[1] - player.radius * 2)
    pipe_length = SCREEN_SIZE[1]
    pipe_width = 50
    pipe_image = pygame.image.load(os.path.join("images", "PipeImage.png"))

    pipe = PipeClass(pipe_x, pipe_y, pipe_width, pipe_length, pipe_image)
    pipes.append(pipe)
    pipe2 = PipeClass(pipe_x, pipe_y - pipe_length - (player.radius * 10), pipe_width, pipe_length,
                      pygame.transform.flip(pipe_image, False, True))
    pipes.append(pipe2)

# Draw screen
def frame_draw(players):
    screen.fill((0, 0, 255))  # Blue background color

    for player in players:
        PLAYER_POSITION = (player.x - player.image.get_width() / 2,
                           player.y - player.image.get_height() / 2)
        screen.blit(player.image, PLAYER_POSITION)

    for pipe in pipes:
        screen.blit(pipe.image, (pipe.x, pipe.y))

# Update instances
def instances_update(players):
    for player in players:
        player.y += GRAVITY

    for pipe in pipes:
        pipe.x -= 2

# Detect if player and pipes collided
def collision_detection(players, ge, nets):
    for player in players:
        player_mask = pygame.mask.from_surface(player.image)
        for pipe in pipes:
            pipe_mask = pygame.mask.from_surface(pipe.image)
            if pipe_mask.overlap(player_mask, (player.x - player.radius - pipe.x, player.y - player.radius - pipe.y)):
                ge[players.index(player)].fitness -= 1
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))

def eval_genomes(genomes, config):
    global pipes, gen  # Ensure you use the global 'pipes' and 'gen' variables
    pipes = []
    gen += 1

    # NEAT
    nets = []
    ge = []
    players = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        # Create a new player instance for each genome
        new_player = PlayerClass(SCREEN_SIZE[0] / 8, SCREEN_SIZE[1] / 2, 30, player_image)
        players.append(new_player)
        ge.append(genome)

    frame_iteration = FPS

    while len(players) > 0:
        frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for x, player in enumerate(players):
            ge[x].fitness += 0.1
            if player.y > (0 + player.radius / 2):
                if pipes:
                    output = nets[x].activate(
                        (player.y, abs(player.y - pipes[0].x), abs(player.y - pipes[0].y)))
                    if output[0] > 0.5:
                        player.jump()
                else:
                    pass
                # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump

            for pipe in pipes:
                if round(player.x) == round(pipe.x):
                    player.score += 1
                    for genome in ge:
                        genome.fitness += 5

            if player.y + player.image.get_height() / 20 >= SCREEN_SIZE[1]:
                ge[x].fitness -= 1
                nets.pop(x)
                ge.pop(x)
                players.pop(x)

        # Detects if player can perform jump
        if player.y > (0 + player.radius / 2):
            pass

        for pipe in pipes:
            if pipe.x <= 0 - pipe.image.get_width():
                pipes.remove(pipe)

        # Detects if player mask and pipe mask collide
        collision_detection(players, ge, nets)

        # Update instances positions
        instances_update(players)

        # Draw the frame
        frame_draw(players)

        # Spawn pipe on intervals
        if frame_iteration % (FPS * 2) == 0:
            spawn_pipe()

        # Flip() the display to put your work on the screen
        pygame.display.flip()
        clock.tick(FPS)  # Limits FPS to a constant

def run(config_file):
    """
    Runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of the config file
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

    # Run for a specified number of generations (e.g., 50).
    while gen < 50:  # Adjust the number of generations as needed
        p.run(eval_genomes)

        # When all players die in one generation, reset the game and start a new generation
        print(f'Generation {gen} completed.')
        # Reset any game-related variables here
        # Call spawn_pipe() or any other initialization functions
        pipes.clear()  # Clear pipes
        # Other game reset logic

    # Show final stats
    print('\nTraining complete.')

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    pygame.quit()
    exit()