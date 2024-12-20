from src.DynaMOSA_Model.algorithm_execution import algorithm_execution
from src.DynaMOSA_Model.OffspringPopulation import OffspringPopulation
import matplotlib.pyplot as plt

#name in paper: Final tests view

class FinalTestsFoundPerIterationPlot:
    def __init__(self, algorithm_execution):
        self.algorithm_execution = algorithm_execution

        #for quick access
        self.tests_in_final_test_suite = self.algorithm_execution.final_test_suite.individuals_in_final_test_suite
        self.corresponding_individuals = [individual.corresponding_individual for individual in self.tests_in_final_test_suite]


    def get_array_of_numbers_of_final_tests_generated_per_iteration(self):
        #initialize a list of zeros with the length of the number of iterations + 1
        #the +1 is because the initial population is also counted as an iteration
        number_of_final_tests_generated_per_iteration = [0] * (len(self.algorithm_execution.iterations) + 1)

        #iterate over the final tests
        for corresponding_individual in self.corresponding_individuals:
            if corresponding_individual.get_location_of_first_occurance() == self.algorithm_execution.initial_population:
                number_of_final_tests_generated_per_iteration[0] += 1
            elif isinstance(corresponding_individual.get_location_of_first_occurance(), OffspringPopulation):
                number_of_final_tests_generated_per_iteration[corresponding_individual.get_location_of_first_occurance().iteration.iteration_number + 1 ] += 1
            else:
                ValueError("The location of the first occurance of the individual is not the initial Population and not an offspring population.")
        return number_of_final_tests_generated_per_iteration
    
    def plot_number_of_final_tests_generated_per_iteration(self, show=False):
        number_of_final_tests_generated_per_iteration = self.get_array_of_numbers_of_final_tests_generated_per_iteration()
        
        # Create a figure and axis
        fig, ax = plt.subplots()
        
        # Plot the data
        ax.plot(range(-1, len(number_of_final_tests_generated_per_iteration) - 1), number_of_final_tests_generated_per_iteration)
        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Number of Final Tests generated')
        #ax.set_title('Number of Final Tests generated per Iteration' + ' for ' + self.algorithm_execution.name)

        if show:
            plt.show()
        
        return fig
        

