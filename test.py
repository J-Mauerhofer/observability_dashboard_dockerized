from algorithm_execution import algorithm_execution


new_algorithm_execution = algorithm_execution(r'C:\Users\Julian Seminar\Desktop\currentLogs\logs.txt')
#print("Iterations:")
#print(new_algorithm_execution.iteration_strings[0][:500])
#print(new_algorithm_execution.iterations[0].population_string[:50])


with open(r'C:\Users\Julian Seminar\Desktop\iterationFromLog.txt', 'w') as file:
    for i in range(30):    
        iter = i
        indi = i

        file.write("\n\nextracted id: " + str(new_algorithm_execution.iterations[iter].population.individuals[indi].id))
        file.write("\nextracted rank: " + str(new_algorithm_execution.iterations[iter].population.individuals[indi].rank))
        file.write("\nextracted fitness: " + str(new_algorithm_execution.iterations[iter].population.individuals[indi].fitness))
        file.write("\nextracted distance: " + str(new_algorithm_execution.iterations[iter].population.individuals[indi].distance))
        file.write("\nextracted code: " + str(new_algorithm_execution.iterations[iter].population.individuals[indi].code))


        file.write("\nindividual: \n\n" + new_algorithm_execution.iterations[iter].population.individuals[indi].raw_string)

