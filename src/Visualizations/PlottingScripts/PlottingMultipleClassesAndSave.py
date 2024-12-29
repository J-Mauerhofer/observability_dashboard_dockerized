import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Add the project base directory (new_clone) to sys.path
project_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_base_dir)

# Standardize all imports to absolute imports
from src.DynaMOSA_Model.algorithm_execution import algorithm_execution
from src.Visualizations.Plots.New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from src.Visualizations.Plots.FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from src.Visualizations.Plots.FrontPlots import FrontPlots
from src.Visualizations.Plots.NewGoalsPerIterationPlot import NewGoalsPerIterationPlot
from src.Visualizations.Plots.GoalsIntersectionPlot import GoalsIntersectionPlot
from src.Visualizations.Plots.AdditionOfNewGoalsPlot import AdditionOfNewGoalsPlot



# Plot the data for one algorithm execution and save to a PDF
def plot_class_with_all_plots(algorithm_execution_instance, pdf):
    plot_count = 0  # Keep track of the number of plots added
    
    # Create instances of the classes using the algorithm execution object
    new_individuals_per_population_plot = New_Individuals_Per_Population_Plot(algorithm_execution_instance)
    final_tests_found_per_iteration_plot = FinalTestsFoundPerIterationPlot(algorithm_execution_instance)
    goals_per_iteration_plot = Goals_per_Iteration_Plot(algorithm_execution_instance)
    goals_intersection_plot = GoalsIntersectionPlot(algorithm_execution_instance)
    front_plots = FrontPlots(algorithm_execution_instance)
    new_goals_per_iteration_plot = NewGoalsPerIterationPlot(algorithm_execution_instance)
    addition_of_new_goals_plot = AdditionOfNewGoalsPlot(algorithm_execution_instance)  # Add the new plot
    
    # Plot the data and save each plot to the PDF
    fig1 = new_individuals_per_population_plot.plot_number_of_individuals_not_present_in_last_population_per_population(show=False)
    if fig1:
        pdf.savefig(fig1)
        plt.close(fig1)
        plot_count += 1
    
    fig2 = final_tests_found_per_iteration_plot.plot_number_of_final_tests_generated_per_iteration(show=False)
    if fig2:
        pdf.savefig(fig2)
        plt.close(fig2)
        plot_count += 1
    
    fig3 = goals_per_iteration_plot.plot_goals_per_iteration(show=False)
    if fig3:
        pdf.savefig(fig3)
        plt.close(fig3)
        plot_count += 1

    fig4 = goals_intersection_plot.plot_goals_intersection(show=False)
    if fig4:
        pdf.savefig(fig4)
        plt.close(fig4)
        plot_count += 1
    
    fig5 = front_plots.plot_front_sizes_in_stacked_area_chart(show=False)
    if fig5:
        pdf.savefig(fig5)
        plt.close(fig5)
        plot_count += 1
    
    fig6 = front_plots.plot_number_of_fronts_per_population(show=False)
    if fig6:
        pdf.savefig(fig6)
        plt.close(fig6)
        plot_count += 1
    
    fig7 = new_goals_per_iteration_plot.plot_number_of_new_goals_per_iteration(show=False)
    if fig7:
        pdf.savefig(fig7)
        plt.close(fig7)
        plot_count += 1

    # Add the new plot as figure 9
    fig8 = addition_of_new_goals_plot.plot_number_of_goals_not_among_initial_goals(show=False)
    if fig8:
        pdf.savefig(fig8)
        plt.close(fig8)
        plot_count += 1

    return plot_count

# Plot the data for all algorithm executions in a given directory and save to PDFs
def plot_all_executions_in_directory(directory_path):
    pdf_path = os.path.join(directory_path, 'all_plots.pdf')
    with PdfPages(pdf_path) as pdf:
        log_files = [file for file in os.listdir(directory_path) if file.endswith(".txt")]
        total_plots = 0
        for log_file in log_files:
            file_path = os.path.join(directory_path, log_file)
            print(f"Now plotting {file_path} and saving to {pdf_path}")
            algorithm_execution_instance = algorithm_execution(file_path)  # Creating the execution object
            total_plots += plot_class_with_all_plots(algorithm_execution_instance, pdf)
        # Check if the PDF is empty and remove it if no figures were added
        if total_plots == 0:
            os.remove(pdf_path)

# Plot the data for all algorithm executions in the given list of directories and save to PDFs
def plot_all_executions_in_directories(directories):
    for directory in directories:
        plot_all_executions_in_directory(directory)

# Plot the data for one algorithm execution and one file name and save to a PDF
def plot_single_execution_in_directory(directory_path, file_name):
    pdf_path = os.path.join(directory_path, f'{file_name}_plots.pdf')
    file_path = os.path.join(directory_path, file_name)
    algorithm_execution_instance = algorithm_execution(file_path)  # Creating the execution object
    
    with PdfPages(pdf_path) as pdf:
        plot_count = plot_class_with_all_plots(algorithm_execution_instance, pdf)
        
        # Check if the PDF is empty and remove it if no figures were added
        if plot_count == 0:
            os.remove(pdf_path)

# List of directories containing log files
directories = [
    #r"C:\Users\Julian Seminar\Desktop\SmartThermostat"
    r"C:\Users\Julian Seminar\Desktop\Examples for paper"
]

# Plot the data and save to PDFs

# Possible actions
plot_all_executions_in_directories(directories)
# plot_single_execution_in_directory(r"C:\Users\Julian Seminar\Desktop\logFilesJgaap", r"jgaapguiDriver$runStatisticalAnalysisDriverLogs.txt")
# plot_single_execution_in_directory(r"C:\Users\Julian Seminar\Desktop\logFilesSugar", r"60_sugar_FSNamespaceContextLogs.txt")
