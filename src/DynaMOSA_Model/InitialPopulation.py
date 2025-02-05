import re
from src.DynaMOSA_Model.Individual_in_Initial_Population import Individual_In_Initial_Population
from typing import List

class InitialPopulation:

    def __init__(self, raw_string, algorithm_execution):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.algorithm_execution = algorithm_execution

        #set the instance variables to the values extracted from the raw string
        self.individual_in_initial_population_strings = self._extract_individual_strings()
        self.individuals_in_initial_population = self._initialize_individuals()
        
    def _initialize_individuals(self) -> List[Individual_In_Initial_Population]:
        """
        Creates Individual_In_Initial_Population objects from the extracted JSON strings.

        Returns:
            List[Individual_In_Initial_Population]: List of individuals in the initial population.
        """
        return [
            Individual_In_Initial_Population(ind_str, self.algorithm_execution)
            for ind_str in self._extract_individual_strings()
        ]

    def _extract_individual_strings(self):
        
        """
        Extracts the individual strings from the raw string.
        """

        pattern = r'{ "id":.*?}\n}'
        matches = re.findall(pattern, self.raw_string, re.DOTALL)
        return matches

    def get_average_fitness(self):
        fitness_sum = 0
        for individual_in_initial_population in self.individuals_in_initial_population:
            fitness_sum += individual_in_initial_population.fitness

        #sum([individual.fitness for individual in self.individuals_in_initial_population])


        return fitness_sum / len(self.individuals_in_initial_population)
    
    def get_average_crowding_distance(self):
        crowding_distance_sum = 0
        for individual_in_initial_population in self.individuals_in_initial_population:
            crowding_distance_sum += individual_in_initial_population.distance

        return crowding_distance_sum / len(self.individuals_in_initial_population)