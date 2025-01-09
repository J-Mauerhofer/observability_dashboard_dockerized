import matplotlib.pyplot as plt
import numpy as np
from src.DynaMOSA_Model.algorithm_execution import algorithm_execution
from src.DynaMOSA_Model.Population import Population


class FrontsView:
    def __init__(self, algorithm_execution):
        self.algorithm_execution = algorithm_execution

        self.populations = [iteration.population for iteration in self.algorithm_execution.iterations]

    def convert_to_2d_array(self, array_of_arrays):
        max_length = max(len(array) for array in array_of_arrays)
        return [array + [0] * (max_length - len(array)) for array in array_of_arrays]

    def plot_number_of_fronts_per_population(self, show=False, title_size=14):
        number_of_fronts_per_population = [len(population.get_front_sizes()) for population in self.populations]
        
        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.plot(range(len(self.populations)), number_of_fronts_per_population)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Number of Fronts')

        # Add title with good spacing and formatting
        ax.set_title('Simple fronts view', 
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

    def plot_front_sizes_in_stacked_area_chart(self, show=False, title_size=14):
        # Initialize the front sizes list
        array_of_front_sizes_lists = [population.get_front_sizes() for population in self.populations]
        _2d_front_sizes_list = self.convert_to_2d_array(array_of_front_sizes_lists)

        # Transpose the 2D list
        as_array = np.array(_2d_front_sizes_list)
        transposed_array = as_array.T
        transposed_list = transposed_array.tolist()

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the stacked area chart
        ax.stackplot(range(len(self.populations)), transposed_list)
        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Front Size')
        #ax.set_title('Front Sizes per Iteration' + ' for ' + self.algorithm_execution.name)

        # Add title with good spacing and formatting
        ax.set_title('Detailed fronts view', 
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




