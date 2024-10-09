import matplotlib.pyplot as plt
from algorithm_execution import algorithm_execution
import numpy as np

class GoalsIntersectionPlot:

    def __init__(self, algorithm_execution):
        self.algorithm_execution = algorithm_execution
        self.iterations = self.algorithm_execution.iterations

    def get_numbers_of_goals_which_are_both_covered_and_uncovered(self):
        numbers_of_goals_which_are_both_covered_and_uncovered = []
        for iteration in self.iterations:
            number_of_goals_which_are_both_covered_and_uncovered = 0
            for goal in iteration.get_covered_goals():
                if goal in iteration.get_uncovered_goals():
                    number_of_goals_which_are_both_covered_and_uncovered += 1
            numbers_of_goals_which_are_both_covered_and_uncovered.append(number_of_goals_which_are_both_covered_and_uncovered)
        return numbers_of_goals_which_are_both_covered_and_uncovered

    def get_numbers_of_goals_which_are_both_covered_and_uncovered_only_goals_which_were_not_part_of_starting_goals(self):
        numbers_of_goals_which_are_both_covered_and_uncovered = []
        for iteration in self.iterations:
            number_of_goals_which_are_both_covered_and_uncovered = 0
            for goal in iteration.get_covered_goals():
                if goal in iteration.get_uncovered_goals() and goal.not_among_goals_at_start:
                    number_of_goals_which_are_both_covered_and_uncovered += 1
            numbers_of_goals_which_are_both_covered_and_uncovered.append(number_of_goals_which_are_both_covered_and_uncovered)
        return numbers_of_goals_which_are_both_covered_and_uncovered

    def plot_goals_intersection(self, show=False):
        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.plot(range(len(self.iterations)), self.get_numbers_of_goals_which_are_both_covered_and_uncovered_only_goals_which_were_not_part_of_starting_goals())
        ax.plot(range(len(self.iterations)), self.get_numbers_of_goals_which_are_both_covered_and_uncovered())

        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Number of Goals which are both covered and uncovered')
        # ax.set_title('Number of Goals which are both covered and uncovered per Iteration' + ' for ' + self.algorithm_execution.name)
        title = 'Number of Goals which are both covered and uncovered' + ' for ' + self.algorithm_execution.name
        ax.set_title(title)
        ax.legend(['Only goals which were not part of starting goals', 'All goals'])

        if show:
            plt.show()
        
        return fig
