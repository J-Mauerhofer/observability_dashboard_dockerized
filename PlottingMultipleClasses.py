from New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from FrontPlots import FrontPlots
from NewGoalsPerIterationPlot import NewGoalsPerIterationPlot
import os


# Plot the data for one filepath
def plot_class_with_all_plots(file_path):
    # Create a new instance of the class
    new_individuals_per_population_plot = New_Individuals_Per_Population_Plot(file_path)
    final_tests_found_per_iteration_plot = FinalTestsFoundPerIterationPlot(file_path)
    goals_per_iteration_plot = Goals_per_Iteration_Plot(file_path)
    front_plots = FrontPlots(file_path)
    new_goals_per_iteration_plot = NewGoalsPerIterationPlot(file_path)
    
    
    # Plot the data
    new_individuals_per_population_plot.plot_number_of_individuals_not_present_in_last_population_per_population()
    final_tests_found_per_iteration_plot.plot_number_of_final_tests_generated_per_iteration()
    goals_per_iteration_plot.plot_goals_per_iteration()
    front_plots.plot_front_sizes_in_stacked_area_chart()
    front_plots.plot_number_of_fronts_per_population()
    new_goals_per_iteration_plot.plot_number_of_new_goals_per_iteration()

# Plot the data for each file
def plot_all_files(file_paths):
    for file_path in file_paths:
        print("now plotting" + str(file_path))
        plot_class_with_all_plots(file_path)



# Manually enter the names of the files here
file_names = ["logFileReference", "logFileRegion","logFileNamedStyle"]

# The folder where the files are located
folder_path = r"C:\Users\Julian Seminar\Desktop\shared ubuntu\SomeLogFilesTemplateIt"

# Initialize the list of file paths
file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]

# Print the file paths
for path in file_paths:
    print(path)

# Plot the data
#plot_class_with_all_plots(r"C:\Users\Julian Seminar\Desktop\SomeLogFilesJiggler\logFileMatrix")
plot_class_with_all_plots(r"C:\Users\Julian Seminar\Desktop\currentLogs\logStackFileNoChangeInMutationRate")
plot_class_with_all_plots(r"C:\Users\Julian Seminar\Desktop\currentLogs\logFileStackMutationRate1")


plot_class_with_all_plots(r"C:\Users\Julian Seminar\Desktop\SomeLogFilesJiggler\logFileComplex")
plot_class_with_all_plots(r"C:\Users\Julian Seminar\Desktop\currentLogs\logfileStack.txt")
plot_all_files(file_paths)

