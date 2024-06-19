import re
from SpecificInformationToIndividual import SpecificInformationToIndividual
from Individual_in_Offspring_Population import IndividualInOffspringPopulation

class OffspringPopulation(SpecificInformationToIndividual):

    def __init__(self, raw_string, iteration):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.iteration = iteration

        #set the instance variables to the values extracted from the raw string
        self.individual_strings = self.extract_individuals_strings_from_raw_string()
        self.individuals = []
        for individual_string in self.individual_strings:
            self.individuals.append(IndividualInOffspringPopulation(individual_string, self))

    def extract_individuals_strings_from_raw_string(self):
        pattern = r'{ "id":.*?} }'
        matches = re.findall(pattern, self.raw_string, re.DOTALL)
        return matches