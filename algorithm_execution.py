import re
from Iteration import Iteration
from InitialPopulation import InitialPopulation
from FinalTestSuite import FinalTestSuite
from Goal import Goal

class algorithm_execution:
    def __init__(self, file_path):
        #read the file
        with open(file_path, 'r') as file:
            self.raw_string = file.read()

        #extract the name of the class and the package from the raw string
        self.name = self.extract_name()

        #extract the total number of test goals for DynaMOSA
        self.total_number_of_test_goals_for_dynamosa = self.extract_total_number_of_test_goals_for_dynamosa()

        #add the goals
        self.goals = self.extract_goals_from_raw_string_and_initialize_goals()
        """
        add the following list of the individuals.
        every time an individual is found during the algorithm execution (mostly happens in the iterations), it is checked whether
        the individual with this id is already in the list of individuals. If no, a new Individual object is created and added to this list
        (self.individuals = []).
        Then, an object of a specific class (e.g. Individual_In_Population) is created. It is added to a list in the Individual object that
        was newly created (and has the same id). The special classes exist because they just contain information about the individual,
        which is specific to the context in which the individual was found (e.g. in a population, in a crossover, in an offspring population, etc.).
        The special classes will have an instance variable that is a reference to the individual object has the same id.

        If the individual with the same id already exists in the list of individuals, no Individual object is created. Instead, the object
        of the special class is created and added to the list of the specific context in the existing Individual object. The special class
        will have an instance variable that is a reference to the existing individual object.
        """
        self.individuals = []
        #add the final test suite
        self.final_test_suite = self.extract_final_test_suite_string_from_raw_string_and_initialize_final_test_suite()
        #add the iterations
        self.iterations = self.extract_iterations_from_raw_string_and_initialize_iterations()
        #add the initial population
        self.initial_population = self.extract_initial_population_from_raw_string_and_initialize_initial_population()

    def extract_final_test_suite_string_from_raw_string_and_initialize_final_test_suite(self):
        # Extract final test suite string
        final_test_suite_string = self.extract_final_test_suite_string_from_raw_string()

        # Initialize final test suite
        final_test_suite = FinalTestSuite(final_test_suite_string, self)

        return final_test_suite

    def extract_name(self):
        # Regular expression pattern to capture the name of the class
        pattern = r'Generating tests for class (.*?)\n'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string)

        # Return the name of the class if found, otherwise throw an exception
        return match.group(1) if match else ValueError("No class name found")
    
    def extract_total_number_of_test_goals_for_dynamosa(self):
        # Regular expression pattern to capture the total number of test goals for DynaMOSA
        pattern = r'Total number of test goals for DYNAMOSA: (\d+)'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string)

        # Return the total number of test goals if found, otherwise throw an exception
        return int(match.group(1)) if match else ValueError("No total number of test goals found")

    def extract_final_test_suite_string_from_raw_string(self):
        # Regular expression pattern to capture the final test suite
        pattern = r'"Final Tests": \[.*?\]'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        # Return the final test suite string if found, otherwise throw an exception
        return match.group() if match else ValueError("No final test suite found")

    def extract_iterations_from_raw_string_and_initialize_iterations(self):
        # Extract iteration strings from raw string
        iteration_strings = self.extract_iteration_strings_from_raw_string()

        # Initialize iterations
        iterations = []
        for iteration_string in iteration_strings:
            iterations.append(Iteration(iteration_string, self))
        
        return iterations

    def extract_iteration_strings_from_raw_string(self):
        # Regular expression pattern to capture iterations
        # Ensure the same iteration number at the start and end
        pattern = r'("Crossovers": {"iteration": (\d+), "crossovers": \[.*?"Archive": { iteration: \2, \[.*?\] \})'


        # Use re.findall to search for all matches of the pattern in self.raw_string
        # The regex should be non-greedy to correctly capture iterations and use DOTALL to span across multiple lines
        matches = re.findall(pattern, self.raw_string, re.DOTALL)
        
        # We only need the full matched string (not the iteration number), so we extract the first group from each match
        iterations = [match[0] for match in matches]
        
        return iterations
    
    def extract_initial_population_from_raw_string_and_initialize_initial_population(self):
        # Extract initial population string
        initial_population_string = self.extract_initial_population_string()

        # Initialize initial population
        initial_population = InitialPopulation(initial_population_string, self)

        return initial_population
    
    def extract_initial_population_string(self):
        # Regular expression pattern to capture the initial population
        pattern = r'"Initial population": popStart\[.*?}\n\]popEnd\n'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        # Return the initial population string if found, otherwise throw an exception
        return match.group() if match else ValueError("No initial population found")


    def extract_all_goal_strings_of_the_algorithm(self):

        #step 1
        #regex pattern to capture the sub-string which contains all goals at the start of the log file
        pattern_for_string_of_all_goals = r'Goals for MultiCriteriaManager: \[\n.*?\]\n\nDependency Graph: \{'

        #apply the regex pattern to the raw string to extract the sub-string
        matches1 = re.findall(pattern_for_string_of_all_goals, self.raw_string, re.DOTALL)
        string_of_all_goals = matches1[0]

        #step 2
        #regex pattern to capture the individual goals in a second step
        pattern_for_individual_goals = r'"(.*?)",?\n'

        #apply the regex pattern to the string_of_all_goals to extract a list of all individual goals in a second step
        matches2 = re.findall(pattern_for_individual_goals, string_of_all_goals, re.DOTALL)
        individual_goals = matches2

        return individual_goals
    
    def extract_goals_from_raw_string_and_initialize_goals(self):
        goals = []
        for goal_string in self.extract_all_goal_strings_of_the_algorithm():
            goals.append(Goal(goal_string))
        return goals
    
    def find_goal_by_string(self, raw_string_of_goal):
        #find the goal object that corresponds to the given raw_string_of_goal
        for goal in self.goals:
            if goal.raw_string == raw_string_of_goal:
                return goal
        raise ValueError(f"No goal found among all goals in the register of all goals for the raw_string {raw_string_of_goal}")
    
    #this function is used to find the individual object that corresponds to the given id in the list of all individual objects.
    def find_individual_by_id(self, id):
        #find the individual object that corresponds to the given id
        for individual in self.individuals:
            if individual.id == id:
                return individual
        return "no individual found for this id"
        #this error is dissabled because the program tries to find the individual obeject and if none exists, it creates a new one
        #raise ValueError(f"No individual found among all individuals in the list of all individuals in the algorithm execution object for the id {id}")