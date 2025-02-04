import re
from src.DynaMOSA_Model.Population import Population
from src.DynaMOSA_Model.Archive import Archive
from src.DynaMOSA_Model.OffspringPopulation import OffspringPopulation
from src.DynaMOSA_Model.Goal import Goal

class Iteration:
    def __init__(self, raw_string, algorithm_execution, verbose=False):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.algorithm_execution = algorithm_execution

        #set the instance variables to the values extracted from the raw string
        self.iteration_number = self.extract_iteration_number()

        self.current_goals = self.extract_current_goals(verbose=verbose)
        self.covered_goals = self.extract_covered_goals(verbose=verbose)
        self.uncovered_goals = self.extract_uncovered_goals(verbose=verbose)
        
        self.number_of_uncovered_goals, self.number_of_covered_goals = self.extract_number_of_covered_and_uncovered_goals()

        self.population_string = self.extract_population_string_from_raw_string()
        self.population = Population(self.population_string, self)

        self.archive_string = self.extract_archive_from_raw_string()
        self.archive = Archive(self.archive_string, self)

        self.offspring_population_string = self.extract_offspring_population_string()
        self.offspring_population = OffspringPopulation(self.offspring_population_string, self)


    #getter methods for the numbers of goals like evosuite outputs them in the log file
    def get_number_of_uncovered_goals_according_to_evosuite(self):
        return self.number_of_uncovered_goals
    
    def get_number_of_covered_goals_according_to_evosuite(self):
        return self.number_of_covered_goals
    
    #getter methods for the number of goals derived by counting the goals
    def get_number_of_uncovered_goals(self):
        return len(self.uncovered_goals)
    
    def get_number_of_covered_goals(self):
        return len(self.covered_goals)
    
    def get_number_of_current_goals(self):
        return len(self.current_goals)
            

    #getter methods for other things
    def get_covered_goals(self):
        return self.covered_goals

    def get_uncovered_goals(self):
        return self.uncovered_goals
    
    def get_current_goals(self):
        return self.current_goals

    


    def extract_number_of_covered_and_uncovered_goals(self):
        # Regex pattern to capture the number of uncovered and covered goals
        pattern = r'"Goals":\s*\{\s*"iteration":\s*\d+,\s*"uncovered":\s*(\d+),\s*"covered":\s*(\d+)'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        if match:
            # Return the number of uncovered and covered goals
            return int(match.group(1)), int(match.group(2))
        else:
            raise ValueError(f"No match found for covered and uncovered goals in iteration {self.iteration_number}")



    def extract_iteration_number(self):
        # Updated regex pattern to capture the iteration number
        pattern = r'"Goals":\s*\{\s*"iteration":\s*(\d+),'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        if match:
            # Return the iteration number
            return int(match.group(1))
        else:
            # If no iteration number is found, an exception is raised
            raise ValueError(f"No match found for iteration number in the log file")



    def extract_current_goals(self, verbose=False):
        # Regex pattern to capture the current goals section
        pattern = r'"current targets": (\[ \[.*?\n\]\})'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        current_goals_string = match.group(1) if match else "No current goals found."

        # Extract individual goals from current_goals_string
        pattern_for_individual_goals = r'"(.*?)",?\n'
        matches = re.findall(pattern_for_individual_goals, current_goals_string, re.DOTALL)
        individual_goal_strings = matches

        # Get a list of goal objects that correspond to the individual goal strings
        individual_goals = []
        for goal_string in individual_goal_strings:
            try:
                # Try to find the goal by string
                goal = self.algorithm_execution.find_goal_by_string(goal_string)
            except ValueError as e:
                # Check if the ValueError message matches the custom one
                if "No goal found among all goals in the register of all goals" in str(e):
                    # Instantiate a new goal object if it's the custom ValueError
                    if verbose:
                        print(f"Custom ValueError caught: {e}")
                    # Create the new goal object and add it to the list of all goals in the algorithm execution
                    goal = Goal(goal_string, True, self.iteration_number)
                    self.algorithm_execution.goals.append(goal)
                else:
                    # Re-raise the ValueError if it's not the custom one
                    raise e
            # Add the found or newly created goal to the list
            individual_goals.append(goal)

        if individual_goals:
            return individual_goals
        else:
            raise ValueError(f"No match found for current goals in iteration {self.iteration_number}")


    def extract_covered_goals(self, verbose=False):
        # Regex pattern to capture the covered goals section
        pattern = r'"covered targets":\s*\[\s*(.*?)\s*\],\s*"current targets":'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        covered_goals_string = match.group(1) if match else "No covered goals found."

        # Extract individual goals from covered_goals_string
        pattern_for_individual_goals = r'"(.*?)"'
        matches = re.findall(pattern_for_individual_goals, covered_goals_string, re.DOTALL)
        individual_goal_strings = matches

        # Get a list of goal objects that correspond to the individual goal strings
        individual_goals = []
        for goal_string in individual_goal_strings:
            try:
                # Try to find the goal by string
                goal = self.algorithm_execution.find_goal_by_string(goal_string)
            except ValueError as e:
                # Check if the ValueError message matches the custom one
                if "No goal found among all goals in the register of all goals" in str(e):
                    # Instantiate a new goal object if it's the custom ValueError
                    if verbose:
                        print(f"Custom ValueError caught: {e}")
                    #create the new goal object and add it to the list of all goals in the algorithm execution
                    goal = Goal(goal_string, True, self.iteration_number)
                    self.algorithm_execution.goals.append(goal)
                else:
                    # Re-raise the ValueError if it's not the custom one
                    raise e
            # Add the found or newly created goal to the list
            individual_goals.append(goal)

        if individual_goals:
            return individual_goals
        else:
            raise ValueError(f"No match found for covered goals in iteration {self.iteration_number}")

    def extract_uncovered_goals(self, verbose=False):
        # Regex pattern to capture the uncovered goals section
        pattern = r'"uncovered targets":\s*\[\s*(.*?)\s*\],\s*"covered targets":'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        uncovered_goals_string = match.group(1) if match else "No uncovered goals found."

        # Extract individual goals from uncovered_goals_string
        pattern_for_individual_goals = r'"(.*?)"'
        matches = re.findall(pattern_for_individual_goals, uncovered_goals_string, re.DOTALL)
        individual_goal_strings = matches

        # Get a list of goal objects that correspond to the individual goal strings
        individual_goals = []
        for goal_string in individual_goal_strings:
            try:
                # Try to find the goal by string
                goal = self.algorithm_execution.find_goal_by_string(goal_string)
            except ValueError as e:
                # Check if the ValueError message matches the custom one
                if "No goal found among all goals in the register of all goals" in str(e):
                    # Instantiate a new goal object if it's the custom ValueError
                    if verbose:
                        print(f"Custom ValueError caught: {e}")
                    # Create the new goal object and add it to the list of all goals in the algorithm execution
                    goal = Goal(goal_string, True, self.iteration_number)
                    self.algorithm_execution.goals.append(goal)
                else:
                    # Re-raise the ValueError if it's not the custom one
                    raise e
            # Add the found or newly created goal to the list
            individual_goals.append(goal)

        if individual_goals:
            return individual_goals
        else:
            raise ValueError(f"No match found for uncovered goals in iteration {self.iteration_number}")


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
        
    def get_average_fitness(self):
        return self.population.get_average_fitness()
    
    def get_average_crowding_distance(self):
        return self.population.get_average_crowding_distance()


    def extract_chromosome_goals_string(log_text: str) -> str:
        """
        Extracts and returns the substring that starts with '"Chromosome Goals": {'
        and ends with the matching closing brace '}' for that block.

        This version attempts to handle braces within double-quoted strings:
        - Tracks whether we are inside a string.
        - Ignores curly braces inside strings.
        - Handles escaped quotes so they don't incorrectly toggle in/out of string mode.

        Raises:
            ValueError: If 'Chromosome Goals' marker is not found,
                        if there's no '{' after the marker,
                        or if matching braces are never closed.

        Returns:
            str: The entire substring from the marker to the matching closing brace.
        """

        marker = '"Chromosome Goals":'
        start_index = log_text.find(marker)
        if start_index == -1:
            raise ValueError("Chromosome Goals marker not found in the provided text.")

        brace_start = log_text.find("{", start_index)
        if brace_start == -1:
            raise ValueError("No opening brace '{' found after Chromosome Goals marker.")

        brace_count = 0
        in_string = False
        escaped = False
        substring_start = brace_start

        # Scan the text starting at the first '{' after the marker
        for i in range(substring_start, len(log_text)):
            char = log_text[i]

            # Check if this character is escaping the next one
            if char == "\\" and not escaped:
                escaped = True
            else:
                # If we see a quote and we're not escaped, toggle string state
                if char == '"' and not escaped:
                    in_string = not in_string

                # Only update brace counts if we're not inside a string
                if not in_string:
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            # Found the matching closing brace
                            return log_text[start_index : i + 1]

                # Reset escaped status if it was set
                escaped = False

        # If we exit the loop, we never closed all braces
        raise ValueError("Matching closing brace '}' for Chromosome Goals block was never found.")
