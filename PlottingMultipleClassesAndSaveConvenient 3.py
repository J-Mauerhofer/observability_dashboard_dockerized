import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from FrontPlots import FrontPlots
from NewGoalsPerIterationPlot import NewGoalsPerIterationPlot

# Plot the data for one file path and save to a PDF
def plot_class_with_all_plots(file_path, axes, row):
    try:
        # Create instances of the classes
        new_individuals_per_population_plot = New_Individuals_Per_Population_Plot(file_path)
    except Exception as e:
        new_individuals_per_population_plot = None
        print(f"Error creating New_Individuals_Per_Population_Plot: {e}")
        
    try:
        final_tests_found_per_iteration_plot = FinalTestsFoundPerIterationPlot(file_path)
    except Exception as e:
        final_tests_found_per_iteration_plot = None
        print(f"Error creating FinalTestsFoundPerIterationPlot: {e}")

    try:
        goals_per_iteration_plot = Goals_per_Iteration_Plot(file_path)
    except Exception as e:
        goals_per_iteration_plot = None
        print(f"Error creating Goals_per_Iteration_Plot: {e}")

    try:
        front_plots = FrontPlots(file_path)
    except Exception as e:
        front_plots = None
        print(f"Error creating FrontPlots: {e}")

    try:
        new_goals_per_iteration_plot = NewGoalsPerIterationPlot(file_path)
    except Exception as e:
        new_goals_per_iteration_plot = None
        print(f"Error creating NewGoalsPerIterationPlot: {e}")

    # Plot the data and save each plot to the axes
    figs = []
    if new_individuals_per_population_plot:
        try:
            figs.append(new_individuals_per_population_plot.plot_number_of_individuals_not_present_in_last_population_per_population(show=False))
        except Exception as e:
            figs.append(None)
            print(f"Error plotting New_Individuals_Per_Population_Plot: {e}")
    else:
        figs.append(None)

    if final_tests_found_per_iteration_plot:
        try:
            figs.append(final_tests_found_per_iteration_plot.plot_number_of_final_tests_generated_per_iteration(show=False))
        except Exception as e:
            figs.append(None)
            print(f"Error plotting FinalTestsFoundPerIterationPlot: {e}")
    else:
        figs.append(None)

    if goals_per_iteration_plot:
        try:
            figs.append(goals_per_iteration_plot.plot_goals_per_iteration(show=False))
        except Exception as e:
            figs.append(None)
            print(f"Error plotting Goals_per_Iteration_Plot: {e}")
    else:
        figs.append(None)

    if front_plots:
        try:
            figs.append(front_plots.plot_front_sizes_in_stacked_area_chart(show=False))
        except Exception as e:
            figs.append(None)
            print(f"Error plotting FrontPlots (stacked area chart): {e}")
        try:
            figs.append(front_plots.plot_number_of_fronts_per_population(show=False))
        except Exception as e:
            figs.append(None)
            print(f"Error plotting FrontPlots (number of fronts per population): {e}")
    else:
        figs.extend([None, None])

    if new_goals_per_iteration_plot:
        try:
            figs.append(new_goals_per_iteration_plot.plot_number_of_new_goals_per_iteration(show=False))
        except Exception as e:
            figs.append(None)
            print(f"Error plotting NewGoalsPerIterationPlot: {e}")
    else:
        figs.append(None)

    for col, fig in enumerate(figs):
        if fig:
            fig.canvas.draw()
            img = fig.canvas.buffer_rgba()
            axes[row, col].imshow(img)
            axes[row, col].set_axis_off()
            plt.close(fig)
        else:
            axes[row, col].text(0.5, 0.5, 'Error: Plot not generated', ha='center', va='center', fontsize=12, color='red')
            axes[row, col].set_axis_off()

# Plot the data for all log files in a given directory and save to PDFs
def plot_all_files_in_directory(directory_path):
    pdf_path = os.path.join(directory_path, 'all_plots_comparison.pdf')
    log_files = [file for file in os.listdir(directory_path) if file.endswith(".txt")]
    num_files = len(log_files)
    if num_files == 0:
        return

    with PdfPages(pdf_path) as pdf:
        fig, axes = plt.subplots(num_files, 6, figsize=(30, 5 * num_files))
        plt.subplots_adjust(wspace=0.05, hspace=0.01)  # Reduce vertical spacing significantly
        for row, file in enumerate(log_files):
            file_path = os.path.join(directory_path, file)
            print(f"Now plotting {file_path} and saving to {pdf_path}")
            plot_class_with_all_plots(file_path, axes, row)
        pdf.savefig(fig)
        plt.close(fig)

# Plot the data for all log files in the given list of directories and save to PDFs
def plot_all_files_in_directories(directories):
    for directory in directories:
        plot_all_files_in_directory(directory)

# List of directories containing log files
directories = [
    #r"C:\Users\Julian Seminar\Desktop\shared ubuntu\SomeLogFilesTemplateIt",
    #r"C:\Users\Julian Seminar\Desktop\SomeLogFilesJiggler",
    #r"C:\Users\Julian Seminar\Desktop\currentLogs"
    #r"C:\Users\Julian Seminar\Desktop\logFilesJgaap"
    #r"C:\Users\Julian Seminar\Desktop\logFilesSugar"
    r"C:\Users\Julian Seminar\Desktop\someLogFilesSquirlSQLIncomplete"

    
]

# Plot the data and save to PDFs
plot_all_files_in_directories(directories)
