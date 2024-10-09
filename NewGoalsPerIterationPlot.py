from Iteration import Iteration
from Goal import Goal
from algorithm_execution import algorithm_execution
import matplotlib.pyplot as plt

#name in paper: New goals view

class NewGoalsPerIterationPlot:

    def __init__(self, algorithm_execution):
        self.algorithm_execution = algorithm_execution
        self.iterations = self.algorithm_execution.iterations

        self.current_goals_per_iteration = [iteration.current_goals for iteration in self.iterations]

        self.new_goals_per_iteration = self.get_new_goals_per_iteration()


    def get_new_goals_per_iteration(self):
        new_goals_per_iteration = []
        for i in range(1, len(self.current_goals_per_iteration)):
            new_goals = []
            for goal in self.current_goals_per_iteration[i]:
                if goal not in self.current_goals_per_iteration[i-1]:
                    new_goals.append(goal)
            new_goals_per_iteration.append(new_goals)
        return new_goals_per_iteration
    

    def plot_number_of_new_goals_per_iteration(self, show=False):
        iteration_numbers = [iteration.iteration_number for iteration in self.iterations]
        # Remove the first iteration because there are no new goals in the first iteration
        iteration_numbers = iteration_numbers[1:]
        number_of_new_goals_per_iteration = [len(new_goals) for new_goals in self.new_goals_per_iteration]

        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.plot(iteration_numbers, number_of_new_goals_per_iteration)
        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Number of New Current Goals')
        #ax.set_title('Number of New Goals per Iteration' + ' for ' + self.algorithm_execution.name)

        if show:
            plt.show()
        
        return fig

