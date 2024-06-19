import re
from Individual_in_Archive import Individual_In_Archive

class Archive:

    def __init__(self, raw_string, iteration):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.iteration = iteration

        #set the instance variables to the values extracted from the raw string
        self.individual_strings = self.extract_individuals_strings_from_raw_string()
        self.individuals = []
        for individual_string in self.individual_strings:
            self.individuals.append(Individual_In_Archive(individual_string, self))

    def extract_individuals_strings_from_raw_string(self):
        #step 1
        # Regex pattern to capture the individuals section within the archive
        pattern = r'"Archive": { iteration: \d+, \[(.*?)\] \}'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        individuals_in_archive_string = match.group(1) if match else "No individuals section found in the archive."

        #step 2
        #regex pattern to capture the individual strings in a second step
        pattern_for_individual_strings = r'"(.*?)",?\n'

        #apply the regex pattern to the individuals_in_archive_string to extract a list of all individual strings in a second step
        matches2 = re.findall(pattern_for_individual_strings, individuals_in_archive_string, re.DOTALL)
        individual_strings = matches2

        return individual_strings


