import matplotlib.pyplot as plt
from src.DynaMOSA_Model.algorithm_execution import algorithm_execution
import numpy as np

class CoveredAndUncoveredGoalsView:

    def __init__(self, algorithm_execution):
        self.algorithm_execution = algorithm_execution
        self.iterations = self.algorithm_execution.iterations

    def get_numbers_of_goals_which_are_both_covered_and_uncovered_only_goals_among_initial_goals(self):
        numbers_of_goals_which_are_both_covered_and_uncovered = []
        for iteration in self.iterations:
            number_of_goals_which_are_both_covered_and_uncovered = 0
            for goal in iteration.get_covered_goals():
                if goal in iteration.get_uncovered_goals() and (not goal.not_among_goals_at_start):
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

    def plot_goals_intersection(self, show=False, title_size=14):
        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.plot(range(len(self.iterations)), self.get_numbers_of_goals_which_are_both_covered_and_uncovered_only_goals_which_were_not_part_of_starting_goals())
        ax.plot(range(len(self.iterations)), self.get_numbers_of_goals_which_are_both_covered_and_uncovered_only_goals_among_initial_goals())

        ax.set_xlabel('Iteration number')
        ax.set_ylabel('Number of Goals which are both covered and uncovered')
        ax.legend(['Goals NOT among initial goals', 'Goals among initial goals'])


        # Add title with good spacing and formatting
        ax.set_title('Covered and uncovered goals view', 
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
