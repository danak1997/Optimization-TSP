from concurrent.futures import ProcessPoolExecutor
from genetic_algorithm import GeneticAlgorithm
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch
from utils import load_input, print_solution

genetic_algorithm_args = [
    50,  # generation size
    32,  # Max cross num
    14,  # Max mutations num
    4,   # Max random chromosomes in a generation
    60,  # Mutation probability in percent
    1,   # parent selection search, 1 - Roulette, 2 - Rank Selection, 3 - Tournament
    -1,  # Max number of iterations
    15,  # Max duration in sec
]

tabu_search_args = [
    500,  # Max size tabu list
    -1,   # Max iterations num
    15,   # Max duration in sec
]

simulated_annealing_args = [
    0.00005,  # Cooling rate 1 - x
    1e-6,     # Initial temperature is sqrt (number_of_ places)
    1e-8,     # Min Min temperature
    60,       # Max duration in sec
]


if __name__ == "__main__":
    print("Set the algorithm parameters in the program.")
    while True:
        entrance, cities, method = load_input()
        if cities is None:
            print("Bad entrance :)")
            continue

        if method.lower() == "vsetky":
            with ProcessPoolExecutor(max_workers=3) as executor:
                solution_GA = executor.submit(GeneticAlgorithm, cities, genetic_algorithm_args)
                solution_SA = executor.submit(SimulatedAnnealing, cities, simulated_annealing_args)
                solution_TABU = executor.submit(TabuSearch, cities, tabu_search_args)
            print_solution(solution_GA.result(), entrance)
            print_solution(solution_SA.result(), entrance)
            print_solution(solution_TABU.result(), entrance)

        elif method.lower() == "ga":
            solution_GA = GeneticAlgorithm(cities, genetic_algorithm_args)
            print_solution(solution_GA, entrance)
        elif method.lower() == "sa":
            solution_SA = SimulatedAnnealing(cities, simulated_annealing_args)
            print_solution(solution_SA, entrance)
        elif method.lower() == "tabu":
            solution_TABU = TabuSearch(cities, tabu_search_args)
            print_solution(solution_TABU, entrance)
