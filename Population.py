import re
import numpy as np
from Individual_In_Population import IndividualInPopulation

class Population:
    def __init__(self, raw_string, iteration):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.iteration = iteration

        #set the instance variables to the values extracted from the raw string
        self.individual_strings = self.extract_individual_in_population_strings_from_population_string()
        self.individuals_in_population = []
        for individual_string in self.individual_strings:
            self.individuals_in_population.append(IndividualInPopulation(individual_string, self))

    def extract_individual_in_population_strings_from_population_string(self):
        pattern = r'{ "id":.*?} }'
        matches = re.findall(pattern, self.raw_string, re.DOTALL)
        return matches


    """ 
    def get_front_sizes(self):
        #get max rank
        max_rank = -1
        for individual_in_population in self.individuals_in_population:
            if individual_in_population.rank > max_rank:
                max_rank = individual_in_population.rank

        if max_rank < 0:
            ValueError(f"Max rank < 0 in {self.iteration.iteration_number}")
            
        #initialize the front sizes array
        front_sizes = np.zeros(max_rank + 1)
        for individual_in_population in self.individuals_in_population:
            front_sizes[individual_in_population.rank] += 1

        for individual_in_population in self.individuals_in_population:
            front_sizes[individual_in_population.rank] += 1

        return front_sizes
    """
    def get_front_sizes(self):
        # get max rank
        max_rank = -1
        for individual_in_population in self.individuals_in_population:
            if individual_in_population.rank > max_rank:
                max_rank = individual_in_population.rank

        if max_rank < 0:
            raise ValueError(f"Max rank < 0 in {self.iteration.iteration_number}")

        # initialize the front sizes list
        front_sizes = [0] * (max_rank + 1)
        for individual_in_population in self.individuals_in_population:
            front_sizes[individual_in_population.rank] += 1

        return front_sizes


