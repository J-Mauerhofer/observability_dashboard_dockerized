import re
from Population import Population
from Archive import Archive
from OffspringPopulation import OffspringPopulation

class Iteration:
    def __init__(self, raw_string, algorithm_execution):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.algorithm_execution = algorithm_execution

        #set the instance variables to the values extracted from the raw string
        self.iteration_number = self.extract_iteration_number()

        self.current_goals = self.extract_current_goals()
        self.number_of_uncovered_goals, self.number_of_covered_goals = self.extract_number_of_covered_and_uncovered_goals()

        self.population_string = self.extract_population_string_from_raw_string()
        self.population = Population(self.population_string, self)

        self.archive_string = self.extract_archive_from_raw_string()
        self.archive = Archive(self.archive_string, self)

        self.offspring_population_string = self.extract_offspring_population_string()
        self.offspring_population = OffspringPopulation(self.offspring_population_string, self)








    def extract_number_of_covered_and_uncovered_goals(self):
        # Regex pattern to capture the number of covered and uncovered goals¨
        pattern = r'"Goals": \{ "iteration": \d+, "uncovered": (\d+), "covered": (\d+), "covered targets":'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        if match:
            # Return the number of covered and uncovered goals
            return int(match.group(1)), int(match.group(2))
        else:
            raise ValueError(f"No match found for covered and uncovered goals in iteration {self.iteration_number}")
        
    def extract_iteration_number(self):
        # Regex pattern to capture the iteration number
        pattern = r'"Crossovers": \{"iteration": (\d+), "crossovers": \['

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        if match:
            # Return the iteration number
            return int(match.group(1))
        else:
            # If no iteration number is found, an exception is raised
            raise ValueError(f"No match found for iteration number in iteration")

    def extract_current_goals(self):
        # Regex pattern to capture the current goals section
        pattern = r'"current targets": (\[.*?\] \})'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        current_goals_string = match.group(1) if match else "No current goals found."

        #extract individual goals from current_goals_string
        pattern_for_individual_goals = r'"(.*?)",?\n'
        matches = re.findall(pattern_for_individual_goals, current_goals_string, re.DOTALL)
        individual_goal_strings = matches

        #get a list of goal objects that correspond to the individual goal strings
        individual_goals = []
        for goal_string in individual_goal_strings:
            individual_goals.append(self.algorithm_execution.find_goal_by_string(goal_string))
        if individual_goals:
            return individual_goals
        else:
            raise ValueError(f"No match found for current goals in iteration {self.iteration_number}")

 

    def extract_population_string_from_raw_string(self):
        # Regex pattern to capture the population section
        # This pattern accounts for matching the 'iteration' number from the beginning of the population section
        pattern = r'("population": {"iteration": \d+, individuals: popStart\[.*?\]popEnd\n })'        
        
        # Use re.search to find the match in the iteration string
        match = re.findall(pattern, self.raw_string, re.DOTALL)
        
        if match:
            # Return the entire matched text including the population data
            # Adjusting the return to just get the content part, not the entire match which includes the 'population' tag
            return match[0]  # You could use `group(2)` to just return the content inside popStart[...popEnd]
        else:
            # If no population data is found, raise an exception
            raise ValueError(f"No match found for population in iteration {self.iteration_number}")
        

    def extract_archive_from_raw_string(self):
        # Regex pattern to capture the archive section

        # This pattern accounts for matching the 'iteration' number from the beginning of the archive section
        pattern = r'("Archive": { iteration: \d+, \[.*?\] })'

        # Use re.search to find the match in the iteration string
        match = re.findall(pattern, self.raw_string, re.DOTALL)

        if match:
            # Return the entire matched text including the archive data
            return match[0]
        else:
            # If no archive data is found, raise an exception
            raise ValueError(f"No match found for archive in iteration {self.iteration_number}")
        
    def extract_offspring_population_string(self):
        # Regex pattern to capture the offspring population section
        # This pattern accounts for matching the 'iteration' number from the beginning of the offspring population section
        pattern = r'("offspring population": {"iteration": \d+, individuals: popStart\[.*?\]popEnd\n })'

        # Use re.search to find the match in the iteration string
        match = re.findall(pattern, self.raw_string, re.DOTALL)
        
        if match:
            # Return the entire matched text including the offspring population data
            return match[0]
        else:
            # If no offspring population data is found, raise an exception
            raise ValueError(f"No offspring population section found in iteration {self.iteration_number}")