import re
from Individual_In_Final_Test_Suite import IndividualInFinalTestSuite

class FinalTestSuite:

    def __init__(self, raw_string, algorithm_execution):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.algorithm_execution = algorithm_execution

        #set the instance variables to the values extracted from the raw string
        self.individual_in_final_test_suite_strings = self.extract_individuals_strings_from_raw_string()
        self.individuals_in_final_test_suite = []
        for individual_string in self.individual_in_final_test_suite_strings:
            self.individuals_in_final_test_suite.append(IndividualInFinalTestSuite(individual_string, self))



    #Todo: implement this method
    def extract_individuals_strings_from_raw_string(self):
        #step 1
        # Regex pattern to capture the individuals section within the final test suite
        pattern = r'"Final Tests": \[(.*?\n)\]'

        # Use re.search to find the match in the raw string
        match = re.search(pattern, self.raw_string, re.DOTALL)

        individual_in_final_test_suite_strings = match.group(1) if match else ValueError("No individuals section found in the final test suite.")

        #step 2
        #regex pattern to capture the individual strings in a second step
        pattern_for_individual_strings = r'"(.*?)",?\n'

        #apply the regex pattern to the individual_in_final_test_suite_strings to extract a list of all individual_in_final_test_suite strings in a second step
        matches2 = re.findall(pattern_for_individual_strings, individual_in_final_test_suite_strings, re.DOTALL)
        individual_strings = matches2

        return individual_strings