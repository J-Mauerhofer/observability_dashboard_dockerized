import re
from src.DynaMOSA_Model.Individual_in_Initial_Population import Individual_In_Initial_Population

class InitialPopulation:

    def __init__(self, raw_string, algorithm_execution):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.algorithm_execution = algorithm_execution

        #set the instance variables to the values extracted from the raw string
        self.individual_in_initial_population_strings = self.extract_individual_in_initial_population_strings_from_raw_string()
        self.individuals_in_initial_population = []
        for individual_in_initial_population_string in self.individual_in_initial_population_strings:
            self.individuals_in_initial_population.append(Individual_In_Initial_Population(individual_in_initial_population_string, algorithm_execution))


    def extract_individual_in_initial_population_strings_from_raw_string(self):
        pattern = r'{ "id":.*?}\n}'
        matches = re.findall(pattern, self.raw_string, re.DOTALL)
        return matches

    def get_average_fitness(self):
        fitness_sum = 0
        for individual_in_initial_population in self.individuals_in_initial_population:
            fitness_sum += individual_in_initial_population.fitness

        return fitness_sum / len(self.individuals_in_initial_population)
    
    def get_average_crowding_distance(self):
        crowding_distance_sum = 0
        for individual_in_initial_population in self.individuals_in_initial_population:
            crowding_distance_sum += individual_in_initial_population.distance

        return crowding_distance_sum / len(self.individuals_in_initial_population)