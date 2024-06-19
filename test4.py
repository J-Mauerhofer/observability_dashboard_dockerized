from algorithm_execution import algorithm_execution
from Goal import Goal


new_algorithm_execution = algorithm_execution(r'C:\Users\Julian Seminar\Desktop\currentLogs\logs.txt')
#print("Iterations:")
#print(new_algorithm_execution.iteration_strings[0][:500])
#print(new_algorithm_execution.iterations[0].population_string[:50])



with open(r'C:\Users\Julian Seminar\Desktop\write.txt', 'w') as file:
   file.write("goal:\n" + new_algorithm_execution.iterations[20].raw_string) 

