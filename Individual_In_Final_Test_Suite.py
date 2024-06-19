import re
from Individual import Individual
from SpecificInformationToIndividual import SpecificInformationToIndividual

class IndividualInFinalTestSuite(SpecificInformationToIndividual):
    
    def __init__(self, raw_string, FinalTestSuite):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.FinalTestSuite = FinalTestSuite

        #set the instance variables to the values extracted from the raw string
        self.id = self.extract_id_from_raw_string()

        #assign the individualInPopulation object to the individual object with the same id.
        #If no such object exists, create a new one and add it to the list of individuals in the algorithm_execution object
        #obtain the individual object and add it to the instance variables
        #add this SpecificInformationToIndividual object to the list of objects in the corresponding_individual object
        algorithm_execution = self.FinalTestSuite.algorithm_execution
        self.handle_matching_with_Individual(algorithm_execution)


    def extract_id_from_raw_string(self):
        #this method extracts the id of the individual from the raw string
        #it just retuns the raw string because the raw string is exatly the id
        return self.raw_string