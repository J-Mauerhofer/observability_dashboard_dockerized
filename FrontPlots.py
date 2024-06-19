import matplotlib.pyplot as plt
import numpy as np
from algorithm_execution import algorithm_execution
from Population import Population


class FrontPlots:
    def __init__(self, file_path):
        self.file_path = file_path
        self.algorithm_execution = algorithm_execution(file_path)

        self.populations = [iteration.population for iteration in self.algorithm_execution.iterations]
    
    """
    def convert_to_2d_array(self, array_of_arrays):
        max_length = max([len(array) for array in array_of_arrays])
        return np.array([np.pad(array, (0, max_length - len(array))) for array in array_of_arrays])
    
    def plot_front_sizes_in_stacked_area_chart(self):
        #initialize the front sizes array
        array_of_front_sizes_arrays = np.array([population.get_front_sizes() for population in self.populations])
        _2d_front_sizes_array = self.convert_to_2d_array(array_of_front_sizes_arrays)

        #plot the stacked area chart
        plt.stackplot(range(len(self.populations)), _2d_front_sizes_array.T)
        plt.xlabel('Iteration')
        plt.ylabel('Front Size')
        plt.title('Front Sizes per Iteration')
        plt.show()
    """
    def plot_number_of_fronts_per_population(self, show=False):
        number_of_fronts_per_population = [len(population.get_front_sizes()) for population in self.populations]
        
        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.plot(range(len(self.populations)), number_of_fronts_per_population)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Number of Fronts')
        ax.set_title('Number of Fronts per Population' + ' for ' + self.algorithm_execution.name)

        if show:
            plt.show()
        
        return fig
    
    def convert_to_2d_array(self, array_of_arrays):
        max_length = max(len(array) for array in array_of_arrays)
        return [array + [0] * (max_length - len(array)) for array in array_of_arrays]

    def plot_front_sizes_in_stacked_area_chart(self, show=False):
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
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Front Size')
        ax.set_title('Front Sizes per Iteration' + ' for ' + self.algorithm_execution.name)

        if show:
            plt.show()
        
        return fig








