from SpecificInformationToIndividual import SpecificInformationToIndividual

class Individual:

    def __init__(self, id):
        self.id = id
        
        #it is not clear if code can always be obtained. This is why It will not be implement yet
        #self.code = None

        """
        the following lists are not fully implemented. At the time of writing this comment, only 
        the occurancesInITERATIONPopulations list is being implemented. The other lists are placeholders for future
        """

        #list of the occurances in the initial population
        self.occurancesInInitialPopulation = []

        #list of the occurances in Iterations
        self.occurancesInITERATIONPopulations = []
        self.occurancesInCrossovers = []
        self.occurancesInOffspringPopulations = []
        self.occurancesInArchives = []

        #list of the occurances in the final test suite
        self.occurancesInFinalTestSuite = []



        #information specific to iterations
        #self.rank = 
        #self.fitness =  
        #self.distance = 
    def add_specific_information_to_individual_to_corresponding_list(self, specific_information_to_individual):
        #add the specific_information_to_individual object to the corresponding list in the individual object
        #check if the specific_information_to_individual object is an instance of a specific class
        from src.DynaMOSA_Model.Individual_In_Population import IndividualInPopulation
        from src.DynaMOSA_Model.Individual_in_Archive import Individual_In_Archive
        from src.DynaMOSA_Model.Individual_in_Offspring_Population import IndividualInOffspringPopulation
        from src.DynaMOSA_Model.Individual_in_Initial_Population import Individual_In_Initial_Population
        from src.DynaMOSA_Model.Individual_In_Final_Test_Suite import IndividualInFinalTestSuite

        if isinstance(specific_information_to_individual, IndividualInPopulation):
            self.occurancesInITERATIONPopulations.append(specific_information_to_individual)
        elif isinstance(specific_information_to_individual, Individual_In_Archive):
            self.occurancesInArchives.append(specific_information_to_individual)
        elif isinstance(specific_information_to_individual, IndividualInOffspringPopulation):
            self.occurancesInOffspringPopulations.append(specific_information_to_individual)
        elif isinstance(specific_information_to_individual, Individual_In_Initial_Population):
            self.occurancesInInitialPopulation.append(specific_information_to_individual)
        elif isinstance(specific_information_to_individual, IndividualInFinalTestSuite):
            self.occurancesInFinalTestSuite.append(specific_information_to_individual)
        #in the future, more elif statements will be added here for the other child classes of SpecificInformationToIndividual
        else:
            raise ValueError("The specific_information_to_individual object is not an instance of a specific class which is handled in this method.")
        

    def get_location_of_first_occurance(self):
        #if this individual was first generated during an iteration (in the offspring population object), return the offspring population object
        #if it was generated during the initial population, return the initial population object

        #check if the individual was first generated during the initial population
        if self.occurancesInInitialPopulation:
            return self.occurancesInInitialPopulation[0].algorithm_execution.initial_population
        
        #check if the individual was first generated during an iteration (in the offspring population object)
        if self.occurancesInOffspringPopulations:
            return self.occurancesInOffspringPopulations[0].offspring_population
        
        #if the individual was not generated during the initial population or an iteration, raise an exception
        raise ValueError("The individual did not occur in the initial population nor in an offspring population.")
