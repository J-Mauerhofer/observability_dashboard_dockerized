import re
from src.DynaMOSA_Model.Individual import Individual
from src.DynaMOSA_Model.SpecificInformationToIndividual import SpecificInformationToIndividual

class IndividualInPopulation(SpecificInformationToIndividual):

    def __init__(self, raw_string, population):
        #set instance variables to the values given in the parameters
        self.raw_string = raw_string
        self.population = population

        #set the instance variables to the values extracted from the raw string
        stats = self.extract_stats()
        self.id = stats["id"]
        self.rank = stats["rank"]
        self.fitness = stats["fitness"] 
        self.distance = stats["distance"]
        self.code = stats["code"]

        #assign the individualInPopulation object to the individual object with the same id.
        #If no such object exists, create a new one and add it to the list of individuals in the algorithm_execution object
        #obtain the individual object and add it to the instance variables
        #add this SpecificInformationToIndividual object to the list of objects in the corresponding_individual object
        algorithm_execution = self.population.iteration.algorithm_execution
        self.handle_matching_with_Individual(algorithm_execution)
        

    def extract_stats(self):
        # Regex pattern to capture stats of this individual, namely id, rank, fitness, distance, and code       
        #match = re.search(r'\{ "id": ([a-zA-Z0-9\-]+), "rank": (-?\d+), "fitness": (\d+(\.\d+)?), "distance": (\d+(\.\d+)?), "code":\{(.*?)\} \}', self.raw_string, re.DOTALL)
        match = re.search(r'\{ "id": ([a-zA-Z0-9\-]+), "rank": (-?\d+), "fitness": (\d+(\.\d+)?|Infinity), "distance": (\d+(\.\d+)?), "code":\{(.*?)\} \}', self.raw_string, re.DOTALL)

        if match:
            stats = {"id": match.group(1), "rank": int(match.group(2)), "fitness": float(match.group(3)), "distance": float(match.group(5)), "code": match.group(7)}
            return stats
        else:
            raise ValueError(f"No match found for individual stats in individual with raw_string{self.raw_string}")