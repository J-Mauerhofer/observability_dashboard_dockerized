from algorithm_execution import algorithm_execution
from Individual import Individual

class Individuals_Per_Population_That_Stay_until_the_end_Plot:

    def __init__(self, file_path):
        self.file_path = file_path
        self.algorithm_execution = algorithm_execution(file_path)
        self.populations = [iteration.population for iteration in self.algorithm_execution.iterations]

        self.individuals_staying_until_the_end_per_Population = self.get_individuals_staying_until_the_end_per_Population()
        

    def get_individuals_staying_until_the_end_per_Population(self):
        individuals_staying_until_the_end_per_Population = []
        for i in range(len(self.populations)):
            individuals_in_current_population = self.populations[i].individual_in_population_objects.corresponding_individual
            individuals_staying_until_the_end = []
            for individual_in_current_population in individuals_in_current_population:
                for current_population in self.populations[i:]:
                    individuals_of_current_population = current_population.individual_in_population_objects.corresponding_individual
                    if individual_in_current_population 
