from utils import haversine
from gps_points import GPSPoints
from deap import base, creator, tools, algorithms
import random
import numpy as np


class GeneticRoutePlanning:
    def __init__(self, gps_points: list[tuple[float, float]]):
        self.gps_points_list = gps_points
        self.toolbox = self.setup_ga_toolbox()

    def total_distance(self, individual) -> tuple[float, None]:
        distance = sum(haversine(self.gps_points_list[individual[i]], self.gps_points_list[individual[i - 1]])
                       for i in range(len(individual)))
        return distance,  # Note the comma to make it a single-element tuple

    def setup_ga_toolbox(self):
        if not hasattr(creator, "FitnessMin"):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()

        toolbox.register("indices", random.sample, range(len(self.gps_points_list)), len(self.gps_points_list))
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", tools.cxOrdered)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("evaluate", lambda ind: self.total_distance(ind))

        return toolbox

    def run_ga(self, ngen=50, pop_size=300):
        population = self.toolbox.population(n=pop_size)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        algorithms.eaSimple(population, self.toolbox, 0.7, 0.2, ngen, stats=stats, halloffame=hof)
        return hof[0], self.toolbox.evaluate(hof[0])[0]
