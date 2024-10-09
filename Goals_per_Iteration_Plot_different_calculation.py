import matplotlib.pyplot as plt
from algorithm_execution import algorithm_execution
import numpy as np

#name in paper: goals progress view

class Goals_per_Iteration_Plot_different_calculation:

    def __init__(self, algorithm_execution):
        self.algorithm_execution = algorithm_execution
        self.iterations = self.algorithm_execution.iterations

        self.number_of_current_goals_per_iteration = self.get_number_of_current_goals_per_iteration()
        self.number_of_covered_goals_per_iteration = self.get_number_of_covered_goals_per_iteration()
        self.number_of_uncovered_goals_per_iteration = self.get_number_of_uncovered_goals_per_iteration()

    def get_number_of_current_goals_per_iteration(self):
        number_of_current_goals_per_iteration = []
        for iteration in self.iterations:
            number_of_current_goals_per_iteration.append(iteration.get_number_of_current_goals())
        return number_of_current_goals_per_iteration
    
    def get_number_of_covered_goals_per_iteration(self):
        number_of_covered_goals_per_iteration = []
        for iteration in self.iterations:
            number_of_covered_goals_per_iteration.append(iteration.get_number_of_covered_goals())
        return number_of_covered_goals_per_iteration
    
    def get_number_of_uncovered_goals_per_iteration(self):
        number_of_uncovered_goals_per_iteration = []
        for iteration in self.iterations:
            number_of_uncovered_goals_per_iteration.append(iteration.get_number_of_uncovered_goals())
        return number_of_uncovered_goals_per_iteration


    """
    def plot_goals_per_iteration(self, show=False):
        # Create a figure and axis
        fig, ax = plt.subplots()
        
        # Plot the data
        ax.plot(range(len(self.iterations)), self.number_of_current_goals_per_iteration, label='Current Goals')
        ax.plot(range(len(self.iterations)), self.number_of_covered_goals_per_iteration, label='Covered Goals')
        ax.plot(range(len(self.iterations)), self.number_of_uncovered_goals_per_iteration, label='Uncovered Goals')
        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Number of Goals')
        
        # Sum of uncovered and covered goals
        sum_of_uncovered_and_covered_goals = np.array(self.number_of_covered_goals_per_iteration) + np.array(self.number_of_uncovered_goals_per_iteration)
        ax.plot(range(len(self.iterations)), sum_of_uncovered_and_covered_goals, label='Sum of covered and uncovered goals')
        #ax.set_title('Goals per Iteration' + ' for ' + self.algorithm_execution.name)
        ax.legend()

        if show:
            plt.show()
        
        return fig

    
    """
    def plot_goals_per_iteration(self, show=False):
        # Create a figure and axis
        fig, ax = plt.subplots()
        
        # Plot the data
        ax.plot(range(len(self.iterations)), self.number_of_current_goals_per_iteration, label='Current Goals')
        ax.plot(range(len(self.iterations)), self.number_of_covered_goals_per_iteration, label='Covered Goals')
        ax.plot(range(len(self.iterations)), self.number_of_uncovered_goals_per_iteration, label='Uncovered Goals')
        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Number of Goals')
        
        # Sum of uncovered and covered goals
        sum_of_uncovered_and_covered_goals = np.array(self.number_of_covered_goals_per_iteration) + np.array(self.number_of_uncovered_goals_per_iteration)
        ax.plot(range(len(self.iterations)), sum_of_uncovered_and_covered_goals, label='Sum of covered and uncovered goals')
        
        # Plot the additional flat line at value 100
        ax.plot(range(len(self.iterations)), [self.algorithm_execution.total_number_of_test_goals_for_dynamosa] * len(self.iterations), label='Total number of goals')
        
        #ax.set_title('Goals per Iteration' + ' for ' + self.algorithm_execution.name)
        ax.legend()

        if show:
            plt.show()
        
        return fig
