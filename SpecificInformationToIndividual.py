
class SpecificInformationToIndividual:
    def __init__(self, id):
        self.id = id

    def handle_matching_with_Individual(self, algorithm_execution):
        from src.DynaMOSA_Model.Individual import Individual
        #match the object with the corresponding individual object and return the corresponding individual object
        corresponding_individual = self.match_with_or_add_to_list_of_individuals_in_algorithm_execution(algorithm_execution)
        self.add_corresponding_individual_to_instance_variables(corresponding_individual)
        self.add_to_specific_list_in_corresponding_individual(corresponding_individual)

    def match_with_or_add_to_list_of_individuals_in_algorithm_execution(self, algorithm_execution):
        from src.DynaMOSA_Model.Individual import Individual
        #assign the individualInPopulation object to the individual object with the same id.
        #If no such object exists, create a new one and add it to the list of individuals in the algorithm_execution object

        #obtain the individual object
        corresponding_individual = "no individual found yet"

        if algorithm_execution.find_individual_by_id(self.id) == "no individual found for this id":
            #create new individual for this id and assign it to corresponding_individual
            newly_created_corresponding_individual = Individual(self.id)
            corresponding_individual = newly_created_corresponding_individual
            #add the newly created individual to the list of individuals in the algorithm_execution object
            algorithm_execution.individuals.append(corresponding_individual)
        elif isinstance(algorithm_execution.find_individual_by_id(self.id), Individual):
            #assign the individual which was found to corresponding_individual
            corresponding_individual = algorithm_execution.find_individual_by_id(self.id)
        else:
            raise ValueError("Critical error in finding the individual object corresponding to the individualInPopulation object.")

        #return the corresponding_individual
        return corresponding_individual

    def add_corresponding_individual_to_instance_variables(self, corresponding_individual):
        from src.DynaMOSA_Model.Individual import Individual
        #assign the corresponding_individual as an instance variable
        self.corresponding_individual = corresponding_individual

    def add_to_specific_list_in_corresponding_individual(self, corresponding_individual):
        from src.DynaMOSA_Model.Individual import Individual
        #add this object to the list of objects in the corresponding_individual object
        corresponding_individual.add_specific_information_to_individual_to_corresponding_list(self)