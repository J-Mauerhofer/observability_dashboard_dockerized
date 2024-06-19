import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from FrontPlots import FrontPlots
from NewGoalsPerIterationPlot import NewGoalsPerIterationPlot

# Plot the data for one file path and save to a PDF
def plot_class_with_all_plots(file_path, pdf):
    plot_count = 0  # Keep track of the number of plots added
    # Create instances of the classes
    new_individuals_per_population_plot = New_Individuals_Per_Population_Plot(file_path)
    final_tests_found_per_iteration_plot = FinalTestsFoundPerIterationPlot(file_path)
    goals_per_iteration_plot = Goals_per_Iteration_Plot(file_path)
    front_plots = FrontPlots(file_path)
    new_goals_per_iteration_plot = NewGoalsPerIterationPlot(file_path)
    
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
    
    fig4 = front_plots.plot_front_sizes_in_stacked_area_chart(show=False)
    if fig4:
        pdf.savefig(fig4)
        plt.close(fig4)
        plot_count += 1
    
    fig5 = front_plots.plot_number_of_fronts_per_population(show=False)
    if fig5:
        pdf.savefig(fig5)
        plt.close(fig5)
        plot_count += 1
    
    fig6 = new_goals_per_iteration_plot.plot_number_of_new_goals_per_iteration(show=False)
    if fig6:
        pdf.savefig(fig6)
        plt.close(fig6)
        plot_count += 1
    
    return plot_count

# Plot the data for all log files in a given directory and save to PDFs
def plot_all_files_in_directory(directory_path):
    pdf_path = os.path.join(directory_path, 'all_plots.pdf')
    with PdfPages(pdf_path) as pdf:
        log_files = [file for file in os.listdir(directory_path) if file.endswith(".txt")]
        total_plots = 0
        for file in log_files:
            file_path = os.path.join(directory_path, file)
            print(f"Now plotting {file_path} and saving to {pdf_path}")
            total_plots += plot_class_with_all_plots(file_path, pdf)
        # Check if the PDF is empty and remove it if no figures were added
        if total_plots == 0:
            os.remove(pdf_path)

# Plot the data for all log files in the given list of directories and save to PDFs
def plot_all_files_in_directories(directories):
    for directory in directories:
        plot_all_files_in_directory(directory)

# List of directories containing log files
directories = [
    #r"C:\Users\Julian Seminar\Desktop\shared ubuntu\SomeLogFilesTemplateIt",
    #r"C:\Users\Julian Seminar\Desktop\SomeLogFilesJiggler",
    r"C:\Users\Julian Seminar\Desktop\currentLogs"
]

# Plot the data and save to PDFs
plot_all_files_in_directories(directories)
