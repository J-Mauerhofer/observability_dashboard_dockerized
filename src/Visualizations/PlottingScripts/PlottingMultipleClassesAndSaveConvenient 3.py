import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from src.Visualizations.Plots.New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from Visualizations.Plots.FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from Visualizations.Plots.FrontPlots import FrontPlots
from src.Visualizations.Plots.NewGoalsPerIterationPlot import NewGoalsPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot_different_calculation import Goals_per_Iteration_Plot_different_calculation
from src.Visualizations.Plots.GoalsIntersectionPlot import GoalsIntersectionPlot
from Visualizations.Plots.AdditionOfNewGoalsPlot import AdditionOfNewGoalsPlot
from DynaMOSA_Model.algorithm_execution import algorithm_execution

# Function to handle the plotting of a single file
def plot_file(file_path, timeout=60):
    try:
        algorithm_execution_instance = algorithm_execution(file_path)
        fig, axes = plt.subplots(3, 3, figsize=(30, 30))  # Create a 3 by 3 grid
        plt.subplots_adjust(wspace=0.05, hspace=0.01)
        plot_class_with_all_plots(algorithm_execution_instance, axes)
        return fig
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# Plot the data for one algorithm execution and save to a PDF
def plot_class_with_all_plots(algorithm_execution_instance, axes):
    figs = []

    try:
        new_individuals_per_population_plot = New_Individuals_Per_Population_Plot(algorithm_execution_instance)
        figs.append(new_individuals_per_population_plot.plot_number_of_individuals_not_present_in_last_population_per_population(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting New_Individuals_Per_Population_Plot: {e}")

    try:
        final_tests_found_per_iteration_plot = FinalTestsFoundPerIterationPlot(algorithm_execution_instance)
        figs.append(final_tests_found_per_iteration_plot.plot_number_of_final_tests_generated_per_iteration(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting FinalTestsFoundPerIterationPlot: {e}")

    try:
        goals_per_iteration_plot = Goals_per_Iteration_Plot(algorithm_execution_instance)
        figs.append(goals_per_iteration_plot.plot_goals_per_iteration(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting Goals_per_Iteration_Plot: {e}")

    try:
        goals_per_iteration_plot_different = Goals_per_Iteration_Plot_different_calculation(algorithm_execution_instance)
        figs.append(goals_per_iteration_plot_different.plot_goals_per_iteration(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting Goals_per_Iteration_Plot_different_calculation: {e}")

    try:
        goals_intersection_plot = GoalsIntersectionPlot(algorithm_execution_instance)
        figs.append(goals_intersection_plot.plot_goals_intersection(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting GoalsIntersectionPlot: {e}")

    try:
        front_plots = FrontPlots(algorithm_execution_instance)
        figs.append(front_plots.plot_front_sizes_in_stacked_area_chart(show=False))
        figs.append(front_plots.plot_number_of_fronts_per_population(show=False))
    except Exception as e:
        figs.extend([None, None])
        print(f"Error plotting FrontPlots: {e}")

    try:
        new_goals_per_iteration_plot = NewGoalsPerIterationPlot(algorithm_execution_instance)
        figs.append(new_goals_per_iteration_plot.plot_number_of_new_goals_per_iteration(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting NewGoalsPerIterationPlot: {e}")

    try:
        addition_of_new_goals_plot = AdditionOfNewGoalsPlot(algorithm_execution_instance)
        figs.append(addition_of_new_goals_plot.plot_number_of_goals_not_among_initial_goals(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting AdditionOfNewGoalsPlot: {e}")

    for col, fig in enumerate(figs):
        row, col = divmod(col, 3)
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
def plot_all_files_in_directory(directory_path, timeout=60):
    pdf_path = os.path.join(directory_path, 'all_plots_comparison.pdf')
    log_files = [file for file in os.listdir(directory_path) if file.endswith(".txt")]
    if not log_files:
        return

    too_large_files = []  # List to track files that took too long

    with PdfPages(pdf_path) as pdf:
        for file in log_files:
            file_path = os.path.join(directory_path, file)
            print(f"Now plotting {file_path} and saving to {pdf_path}")
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(plot_file, file_path, timeout)
                try:
                    fig = future.result(timeout=timeout)
                    if fig:
                        pdf.savefig(fig)
                        plt.close(fig)
                    else:
                        too_large_files.append(file)
                except FuturesTimeoutError:
                    print(f"File {file} took too long to generate.")
                    too_large_files.append(file)
                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    ax.text(0.5, 0.5, f"Error: {file}\ntook too long to generate", ha='center', va='center', fontsize=12, color='red')
                    ax.set_axis_off()
                    pdf.savefig(fig)
                    plt.close(fig)

    # If there are large files, generate a second PDF with their names
    if too_large_files:
        larger_pdf_path = os.path.join(directory_path, 'larger_files.pdf')
        with PdfPages(larger_pdf_path) as pdf:
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.text(0.5, 0.9, "Files that took too long to generate:", ha='center', va='top', fontsize=16, weight='bold')
            for i, file in enumerate(too_large_files, start=1):
                ax.text(0.5, 0.9 - i * 0.05, file, ha='center', va='top', fontsize=12)
            ax.set_axis_off()
            pdf.savefig(fig)
            plt.close(fig)

# Plot the data for all log files in the given list of directories and save to PDFs
def plot_all_files_in_directories(directories, timeout=60):
    for directory in directories:
        plot_all_files_in_directory(directory, timeout=timeout)

# List of directories containing log files
directories = [
    #r"C:\Users\Julian Seminar\Desktop\36_schemaspy_logFiles"
    #r"C:\Users\Julian Seminar\Desktop\shared ubuntu\SmartThermostatChatGPT"
    #r"C:\Users\Julian Seminar\Desktop\36_schemy_copy"
    #r"C:\Users\Julian Seminar\Desktop\log files in general\new log files september"
    #r"C:\Users\Julian Seminar\Desktop\Log files of demos in the paper",
    r"C:\Users\Julian Seminar\Desktop\Examples for paper"
    ]

# Plot the data and save to PDFs
plot_all_files_in_directories(directories)
