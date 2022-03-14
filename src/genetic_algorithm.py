import random
import timeit
from utils import fitness


class GeneticAlgorithm(list):
    def __init__(self, cities, args):
        self.name = "GENETIC ALGORITHM..."
        self.parse_args(args)  # handle arguments
        iteration = 0
        init_time = timeit.default_timer()
        generation = random_generation(cities, self.generation_size)  # first random generation
        generation.sort(reverse=True)  # The highest fitness first

        while not self.stop(iteration, init_time):
            cross_generation = cross(generation, self.cross_num, self.parent_selection_method)
            mutation_generation = Mutation(cross_generation, self.mutations_num, self.probability_of_mutation)
            rg = random_generation(cities, self.random_num)
            generation = self.choose_best(
                generation,
                cross_generation,
                mutation_generation,
                rg,
                self.generation_size,
            )
            iteration += 1

        self.run_time = timeit.default_timer() - init_time
        list.__init__(self, generation[0])  # returns the list of lists with the best result

    # Survival of the Fittest, removes the worst of all generated
    def choose_best(self, best, cross, mutation, random, size):
        survived = best + cross + mutation + random
        survived.sort(reverse=True)
        return survived[0:size]  # cuts from 0 to x

    # turns off after x iterations or after time has elapsed
    def stop(self, iteration, start):
        return iteration == self.max_iterations or timeit.default_timer() - start > self.max_duration

    def parse_args(self, args):
        self.generation_size = args[0]
        self.cross_num = args[1]
        self.mutations_num = args[2]
        self.random_num = args[3]
        self.probability_of_mutation = args[4]
        self.parent_selection_method = args[5]
        self.max_iterations = args[6]
        self.max_duration = args[7]


# Introduces Chromosome - vector of site visits (genes)
class Individual(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        self.price = fitness(args[0]) ** -1  # inverted value

    def __lt__(self, other):
        return self.price < other.price


class cross(list):
    def __init__(self, generation, size, parent_selection_method):
        self.parent_selection_method = parent_selection_method
        list.__init__(self, self.cross(generation, size))

    def cross(self, generation, size):
        deti = []
        for _ in range(size):
            parents = select_parent(generation, self.parent_selection_method)
            child = self.two_point_cross(parents)
            deti.append(Individual(child))
        return deti

    # two-point cross
    def two_point_cross(self, parents):
        start, end = random_section(parents[0])  # random section is put in the right place
        tmp = [x for x in parents[1] if x not in parents[0][start:end]]  # remove dup
        child = tmp[0:start] + parents[0][start:end] + tmp[start:]  # fill in the rest of the parent
        return child


class Mutation(list):
    def __init__(self, generation, size, probability_of_mutation):
        self.probability_of_mutation = probability_of_mutation  # how many percent will I mutate the children
        list.__init__(self, self.mutation(generation, size))

    # mutates the element by turning a random section in the permutation
    def mutation(self, generation, size):
        mutated = []
        for _ in range(size):
            chance = random.randint(1, 100)
            if chance <= self.probability_of_mutation:
                parent = random.randint(0, len(generation) - 1)
                child = self.section_rotation_mutation(generation[parent])
                mutated.append(Individual(child))
        return mutated

    def section_rotation_mutation(self, parent):
        start, end = random_section(parent)  # selects a section and turns it
        child = parent[0:start] + list(reversed(parent[start:end])) + parent[end:]
        return child


class select_parent(list):
    def __init__(self, generation, parent_selection):
        self.parents_selection = parent_selection
        list.__init__(self, self.parents_selection_method(generation))

    def parents_selection_method(self, generation):
        if self.parents_selection == 1:
            return self.roulette(generation)
        if self.parents_selection == 2:
            return self.rank_selection(generation)
        if self.parents_selection == 3:
            return self.tournament(generation)

    # based on moderation with fitness, the parent chooses
    def roulette(self, generation):
        total_fitness = 0  # start the roulette
        for individual in generation:
            total_fitness += individual.price
        parents = []
        for _ in range(2):  # select two parents
            start = random.uniform(0, total_fitness)
            count = 0
            for individual in generation:
                count += individual.price
                if count >= start:  # exceeded subtotal
                    parents.append(individual)
                    break
        return parents

    # basis of moderation with the order in which the parent is chosen
    def rank_selection(self, generation):
        total_fitness = (len(generation) + 1) * len(generation) / 2
        parents = []
        for _ in range(2):  # select two parents
            start = random.uniform(0, 1)
            count = 0
            for i, individual in enumerate(reversed(generation), start=1):
                count += i / total_fitness
                if count >= start:  # exceeded subtotal
                    parents.append(individual)
                    break
        return parents

    # randomly select two candidates and cross the worst one
    def tournament(self, generation):
        n = len(generation)
        parents = []
        for _ in range(2):
            first = random.randint(0, n - 1)
            types = random.randint(0, n - 1)
            if first < types:
                parents.append(generation[first])
            else:
                parents.append(generation[types])
        return parents


# randomly shuffling places on the map
def random_generation(cities, size):
    generation = []
    for _ in range(size):
        chromozom = cities.copy()  # new vector
        random.shuffle(chromozom)  # random permutation
        generation.append(Individual(chromozom))
    return generation


# selects a section in the city visit permutation, min length 2
def random_section(state):
    start = random.randint(0, len(state) - 2)
    end = random.randint(start + 1, len(state) - 1)
    return start, end
