import random

POPULATION_COUNT: int = 100
GENOME_LENGTH: int = 32
MUTATION_CHANCE: float = 0.001
CROSSOVER_RATE: float = 0.5

class Solution:

    def __init__(self, new_genome: list, new_fitness: int):
        self.genome = new_genome
        self.fitness = new_fitness

def main():

    print(" ~ MaxOnes ~ ")
    print("Population: " + str(POPULATION_COUNT))
    print("Genome Length: " + str(GENOME_LENGTH))
    print("Mutation Chance: " + str(MUTATION_CHANCE))
    print("Crossover Rate: " + str(CROSSOVER_RATE))

    grand_parents = []

    for i in range(POPULATION_COUNT):
        new_genome: list = []
        for x in range(GENOME_LENGTH):
            new_bit: int = random.randint(0, 1)
            new_genome.append(new_bit)

        new_fitness: int = get_fitness(new_genome)
        new_solution = Solution(new_genome, new_fitness)
        grand_parents.append(new_solution)

    mate(grand_parents, 1)


def get_fitness(genome: list):
    fitness: int = 0
    for x in genome:
        if x == 1:
            fitness += 1
    return fitness


def mate(parents: list, generation: int):
    record_fitness: int = 0
    average_fitness: float = 0
    identical_genomes: int = 0

    for x in range(POPULATION_COUNT):
        mates: list = select_mates(parents)
        crossover_index: int = random.randint(0, GENOME_LENGTH - 1)
        child_genome: list = []
        for i in range(2): # for each mate
            for n in range(int(GENOME_LENGTH * abs(i - CROSSOVER_RATE))): # stupid but incorporates crossover rate
                child_genome.append(mates[i].genome[crossover_index % GENOME_LENGTH])
                crossover_index += 1
        child_genome = mutate(child_genome)
        new_fitness: int = get_fitness(child_genome)
        if new_fitness == GENOME_LENGTH:
            print("Generation " + str(generation) + ": reached convergence!")
            return

        average_fitness += new_fitness
        if new_fitness > record_fitness:
            record_fitness = new_fitness
        old_solution: Solution = parents.pop(0)
        del old_solution
        parents.append(Solution(child_genome, new_fitness))
    for x in range(POPULATION_COUNT):
        for y in range(POPULATION_COUNT - 1):
            if parents[x].genome == parents[(x + y + 1) % POPULATION_COUNT].genome:
                identical_genomes += 1
                break

    average_fitness /= float(POPULATION_COUNT)

    print("Generation " + str(generation)
          + ": highest fitness: " + str(record_fitness)
          + ", average fitness: " + str(average_fitness)
          + ", % of population with identical genomes: " + str(float(identical_genomes) / float(POPULATION_COUNT))
          )

    generation += 1
    if generation <= 100:
        mate(parents, generation)
    else:
        print("Reached maximum generation without convergence")


def select_mates(solutions: list):
    sum_fitness: int = 0
    new_parents: list = []
    wheel: list = []
    for x in solutions:
        for y in range(x.fitness):
            wheel.append(x)
    rand_index1: int = random.randint(0, len(wheel) - 1)
    rand_index2: int = random.randint(0, len(wheel) - 1)
    while wheel[rand_index1] == wheel[rand_index2]:
        rand_index2 = random.randint(0, len(wheel) - 1)

    return [wheel[rand_index1], wheel[rand_index2]]


def mutate(genome: list):
    for i in range(len(genome)):
        if random.random() <= MUTATION_CHANCE:
            genome[i] = abs(genome[i] - 1)  # funny way to toggle between 1 and 0
    return genome


main()
