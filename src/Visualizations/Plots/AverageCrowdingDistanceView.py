import matplotlib.pyplot as plt

class AverageCrowdingDistanceView:
    def __init__(self, algorithm_execution):
        self.algorithm_execution = algorithm_execution

    def get_average_crowding_distance_per_iteration_and_for_initial_population(self):
        average_crowding_distance_per_iteration_and_initial_population = []
        #add average crowding distance for initial population
        average_crowding_distance_per_iteration_and_initial_population.append(self.algorithm_execution.initial_population.get_average_crowding_distance())
        #add average crowding_distance for each iteration
        for iteration in self.algorithm_execution.iterations:
            average_crowding_distance_per_iteration_and_initial_population.append(iteration.get_average_crowding_distance())

        return average_crowding_distance_per_iteration_and_initial_population
    

    def plot_average_crowding_distance(self, show=False, title_size=14):
        average_crowding_distance_per_iteration_and_initial_population = self.get_average_crowding_distance_per_iteration_and_for_initial_population()
        iteration_numbers = [-1] + [iteration.iteration_number for iteration in self.algorithm_execution.iterations]

        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.plot(iteration_numbers, average_crowding_distance_per_iteration_and_initial_population)
        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Average Crowding Distance')

        # Add title with good spacing and formatting
        ax.set_title('Average crowding distance view', 
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