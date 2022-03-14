import random
import timeit
import math

from utils import fitness


class SimulatedAnnealing(list):
    def __init__(self, cities, args):
        self.name = "SIMULATED ANNEALING..."
        self.parse_args(args)  # handle arguments
        init_time = timeit.default_timer()
        schedule = Schedule(self.cooling, self.min_temperature, self.max_temperature)  # temperature schedule
        random.shuffle(cities)  # random vector
        current = condition(cities)
        temperature = schedule.initial_temperature

        while not self.stop(temperature, schedule.min_temperature, init_time):
            neighbor = self.select_follower(current)
            delta = neighbor.fitness - current.fitness
            if delta > 0 or self.probability(delta, temperature):
                current = neighbor  # only accept if the temperature is better or low enough
            temperature *= schedule.cooling

        self.run_time = timeit.default_timer() - init_time
        list.__init__(self, current)

    # selects a random section and rotates it
    def select_follower(self, Condition):
        start, end = random_section(Condition)  # selects a section and turns it
        child = Condition[0:start] + list(reversed(Condition[start:end])) + Condition[end:]
        return condition(child)

    # the probability function of adopting a worse solution
    def probability(self, delta, temperature):
        chance = math.exp(delta / temperature)
        rand = random.uniform(0, 1)
        return True if chance >= rand else False

    def stop(self, temperature, min_temperature, start):
        return temperature < min_temperature or timeit.default_timer() - start > self.max_duration

    def parse_args(self, args):
        self.cooling = args[0]
        self.max_temperature = args[1]
        self.min_temperature = args[2]
        self.max_duration = args[3]


class condition(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        self.fitness = fitness(args[0]) ** -1  # inverse value


class Schedule:
    def __init__(self, cooling, min_temperature, max_temperature):
        self.cooling = 1 - cooling
        self.initial_temperature = max_temperature
        self.min_temperature = min_temperature


# selects a section in the city visit permutation, min length 2
def random_section(state):
    start = random.randint(0, len(state) - 2)
    end = random.randint(start + 1, len(state) - 1)
    return start, end
