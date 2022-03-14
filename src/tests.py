from genetic_algorithm import GeneticAlgorithm
from utils import print_solution


def GA_testing(cities, genetic_algorithm_args):
    """
    tmp_args = default_args_GA.copy()
    genetic_algorithm_args[5] = 3

    for i in range(4):
        tmp_args[i] *= 5  # naConditionenia
    solution_genetic = GeneticAlgorithm(cities, tmp_args)
    print_solution(solution_genetic)  # print info

    """
    for i in range(1, 4):
        genetic_algorithm_args[5] = i
        tmp_args = genetic_algorithm_args.copy()

        solution_genetic = GeneticAlgorithm(cities, genetic_algorithm_args)
        print_solution(solution_genetic)  # print info

        for i in range(4):
            tmp_args[i] *= 5

        solution_genetic = GeneticAlgorithm(cities, tmp_args)
        print_solution(solution_genetic)  # print info
