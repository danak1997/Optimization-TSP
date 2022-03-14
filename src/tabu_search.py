import random
import timeit
from utils import fitness


class TabuSearch(list):
    def __init__(self, cities, args):
        self.name = "TABU SEARCH..."
        self.parse_args(args)  # process arguments
        random.shuffle(cities)  # generating a random vector
        global_max = cities
        best_candidate = cities
        tabu_list = [cities]  # List of prohibited Conditions
        not_improved = 0  # iteration, after x not improved stop
        init_time = timeit.default_timer()
        while not self.stop(not_improved, init_time):
            followers = self.generate_followers(best_candidate)
            best_candidate = self.find_best_candidate(followers, tabu_list)

            best_candidate_fitness = fitness(best_candidate)
            global_max_fitness = fitness(global_max)

            if best_candidate_fitness < global_max_fitness:
                global_max = best_candidate
                not_improved = 0

            tabu_list.append(best_candidate)
            if len(tabu_list) > self.max_tabu_size:
                tabu_list.pop(0)
            not_improved += 1
        self.run_time = timeit.default_timer() - init_time
        list.__init__(self, global_max)

    # will generate max only (n) followers by selecting a random exchange point with all
    def generate_followers(self, Condition):
        rand = random.randint(0, len(Condition) - 1)
        followers = []
        for i in range(0, len(Condition)):
            if i != rand:
                follower = Condition.copy()
                follower[i], follower[rand] = follower[rand], follower[i]
                followers.append(follower)
        return followers

    # best Condition among followers, if not in the taboo
    def find_best_candidate(self, followers, tabu_list):
        candidate_tabu = followers[0]
        for follower in followers:
            if follower not in tabu_list and fitness(follower) < fitness(candidate_tabu):
                candidate_tabu = follower
        return candidate_tabu

    def stop(self, not_improved, start):
        return not_improved == self.max_iterations or timeit.default_timer() - start > self.max_duration

    def parse_args(self, args):
        self.max_tabu_size = args[0]
        self.max_iterations = args[1]
        self.max_duration = args[2]
