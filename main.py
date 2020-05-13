import os
import pygame
import neat
from data.bird import Bird
from data.pipe import Pipe
pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
font = pygame.font.SysFont('agencyfb', 30)
font1 = pygame.font.SysFont('agencyfb', 25)

score_updated = score = None
gen = 0


def main(genomes, config):
    global score, score_updated, gen
    gen += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(screen, 40, HEIGHT//2))
        g.fitness = 0
        ge.append(g)

    pipes = []
    pipes.append(Pipe(screen))

    score_updated = False
    score = 0

    frame_count = 0
    while True:
        clock.tick(60)

        # if no birs left return
        if len(birds) <= 0:
            break

        frame_count += 1
        if frame_count % 150 == 0:
            pipes.append(Pipe(screen))
            score_updated = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((51, 51, 51))
        score_text = font.render(f'Score: {score}', 1, (200, 200, 200))
        screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 0))
        gen_text = font1.render(f'Gen: {gen}', 1, (200, 200, 200))
        screen.blit(gen_text, (5, 0))
        pop_text = font1.render(f'Pop: {len(birds)}', 1, (200, 200, 200))
        screen.blit(pop_text, (5, gen_text.get_height()))

        for x, bird in enumerate(birds):
            bird.update()
            bird.show()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (bird.y, abs(bird.y - pipes[0].top), abs(bird.y - pipes[0].bottom)))

            if output[0] > 0.5:
                bird.up()

        for x, bird in enumerate(birds):
            if bird.fall():
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

            if bird.y <= 0:
                ge[x].fitness -= 5

        for i in range(len(pipes)-1, -1, -1):
            pipes[i].update()

            # Get rid of the bird which hits pipe
            for x, bird in enumerate(birds):
                if bird.hits(pipes[i]):
                    # ge[x].fitness -= 1  # decrease fitness which gene hits pipe
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if bird.passed(pipes[i]) and not score_updated:
                    # increase fitness which gene goes through the pipe
                    for g in ge:
                        g.fitness += 5
                    # ge[x].fitness += 5

                    score += 1
                    score_updated = True

            pipes[i].show(False)

            if pipes[i].offscreen():
                pipes.pop(i)

        pygame.display.update()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)

    # Statistics Report
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # 50 generations -> call fitness function 'main' 50 times
    winner = population.run(main, 150)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
