import matplotlib.pyplot as plt
from src.DynaMOSA_Model.algorithm_execution import algorithm_execution
import numpy as np

#name in paper: New Individuals view

class NewIndividualsView:

    def __init__(self, algorithm_execution):
        self.algorithm_execution = algorithm_execution
        self.populations = [iteration.population for iteration in self.algorithm_execution.iterations]

        self.individuals_not_present_in_last_population = self.get_individuals_not_present_in_last_population()

    
    def get_individuals_not_present_in_last_population(self):
        individuals_not_present_in_last_population_for_each_population = []
        for i in range(1, len(self.populations)):
            individuals_in_current_population = self.algorithm_execution.iterations[i].population.individuals_in_population
            individuals_in_last_population = self.algorithm_execution.iterations[i-1].population.individuals_in_population

            individuals_not_present_in_last_population = []
            for individual_in_current_population in individuals_in_current_population:
                found_yet = False
                for individual_in_last_population in individuals_in_last_population:
                    if individual_in_current_population.id == individual_in_last_population.id:
                        found_yet = True
                        break
                if not found_yet:
                    individuals_not_present_in_last_population.append(individual_in_current_population)
            individuals_not_present_in_last_population_for_each_population.append(individuals_not_present_in_last_population)
        return individuals_not_present_in_last_population_for_each_population
    
    def plot_number_of_individuals_not_present_in_last_population_per_population(self, show=False, title_size=14):
        population_sizes = [len(population.individuals_in_population) for population in self.populations]

        # Create a figure and axis
        fig, ax = plt.subplots()

        for i in range(len(self.individuals_not_present_in_last_population)):
            ax.plot(i, len(self.individuals_not_present_in_last_population[i]), 'r.')
            #ax.plot(i, population_sizes[i], 'r.')
            
        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Number of Individuals not present in last Population')
        #ax.set_title('Number of Individuals not present in last Population per Population' + ' for ' + self.algorithm_execution.name)

        # Add title with good spacing and formatting
        ax.set_title('New Individuals View', 
                    pad=20,        # Add padding above the title
                    fontsize=title_size,   # Larger font size
                    fontweight='bold')  # Make it bold
        
        # Add class name as subtitle with smaller font
        ax.text(0.5, 1.02,         # Position it above the main title
                self.algorithm_execution.name,
                horizontalalignment='center',
                transform=ax.transAxes,
                fontsize=10,
                style='italic')

        if show:
            plt.show()
        
        return fig
