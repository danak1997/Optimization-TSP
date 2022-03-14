import math

optimal = {
    "default20": 896,
    "wi29": 27601,
    "att48": 33522,
    "berlin52": 7544,
}


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def load_input():
    print("End [e]")
    print("Choose the city map: [default20] [wi29] [att48] [berlin52]")
    print("or [own] from the tests-own.txt file")
    entrance = input()
    if entrance in ("default20", "wi29", "att48", "berlin52"):
        path = "tests/" + entrance + ".txt"
    elif entrance == "own":
        path = "tests/own.txt"
    elif entrance == "e":
        print("I'm quitting")
        quit()
    else:
        return [None] * 3
    cities = parse_input(f"./{path}")
    print(f"{path} Number of places:{len(cities)}")
    print("Choose your method:")
    print("Genetic Algorithm[GA]")
    print("Simulated annealing[SA]")
    print("Tabu search[TABU]")
    print("All at once [VSETKY]")
    method = input()
    if method.lower() not in ("ga", "sa", "tabu", "vsetky"):
        return [None] * 3
    print("Loading...")
    return entrance, cities, method


def parse_input(path):
    cities = []
    with open(path, "r") as file:
        for line in file:
            coordinates = line.strip().split()
            cities.append(list(map(float, coordinates)))
    return [City(city[0], city[1]) for city in cities]


def fitness(Condition):
    result = 0
    for i in range(len(Condition) - 1):
        result += euclidian_d(Condition[i], Condition[i + 1])
    result += euclidian_d(Condition[-1], Condition[0])
    return result


def euclidian_d(a, b):
    result = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
    return result


def print_solution(solution, entrance):
    solution_price = int(round(fitness(solution)))
    opt = entrance in optimal
    for city in solution:
        print(f"{round(city.x, 2)} \t {round(city.y, 2)}")
    print(solution.name)
    print(f"Solution price: {solution_price}")
    if opt is True:
        print(f"Optimalne solution: {optimal.get(entrance)}")
        print(f"Percent: {((optimal.get(entrance) / solution_price) * 100):.3f}%")
    print(f"Search found: {solution.run_time}")
