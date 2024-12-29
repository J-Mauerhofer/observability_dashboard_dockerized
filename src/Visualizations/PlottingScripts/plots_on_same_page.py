import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import sys

# Add the project base directory (new_clone) to sys.path
project_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_base_dir)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from src.Visualizations.Plots.New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from src.Visualizations.Plots.FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from src.Visualizations.Plots.FrontPlots import FrontPlots
from src.Visualizations.Plots.NewGoalsPerIterationPlot import NewGoalsPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot_different_calculation import Goals_per_Iteration_Plot_different_calculation
from src.Visualizations.Plots.GoalsIntersectionPlot import GoalsIntersectionPlot
from src.Visualizations.Plots.AdditionOfNewGoalsPlot import AdditionOfNewGoalsPlot
from src.DynaMOSA_Model.algorithm_execution import algorithm_execution

# Mapping of plot names to their respective methods
PLOT_METHODS = {
    "New_Individuals_Per_Population_Plot": New_Individuals_Per_Population_Plot.plot_number_of_individuals_not_present_in_last_population_per_population,
    "FinalTestsFoundPerIterationPlot": FinalTestsFoundPerIterationPlot.plot_number_of_final_tests_generated_per_iteration,
    "Goals_per_Iteration_Plot": Goals_per_Iteration_Plot.plot_goals_per_iteration,
    "Goals_per_Iteration_Plot_different_calculation": Goals_per_Iteration_Plot_different_calculation.plot_goals_per_iteration,
    "GoalsIntersectionPlot": GoalsIntersectionPlot.plot_goals_intersection,
    "FrontPlots": [FrontPlots.plot_front_sizes_in_stacked_area_chart, FrontPlots.plot_number_of_fronts_per_population],
    "NewGoalsPerIterationPlot": NewGoalsPerIterationPlot.plot_number_of_new_goals_per_iteration,
    "AdditionOfNewGoalsPlot": AdditionOfNewGoalsPlot.plot_number_of_goals_not_among_initial_goals,
}

# Function to handle the plotting of a single file with selected plots
def plot_file(file_path, selected_plots, timeout=60):
    try:
        algorithm_execution_instance = algorithm_execution(file_path)
        fig, axes = plt.subplots(3, 3, figsize=(30, 30))  # Create a 3 by 3 grid
        plt.subplots_adjust(wspace=0.05, hspace=0.01)
        
        # Generate plots dynamically based on `selected_plots`
        for idx, plot_name in enumerate(selected_plots):
            row, col = divmod(idx, 3)
            plot_function = PLOT_METHODS.get(plot_name)
            
            if isinstance(plot_function, list):  # Handle multiple plots for one name
                for func in plot_function:
                    try:
                        plot = func(algorithm_execution_instance, show=False)
                        if plot:
                            plot.canvas.draw()
                            img = plot.canvas.buffer_rgba()
                            axes[row, col].imshow(img)
                            axes[row, col].set_axis_off()
                            plt.close(plot)
                    except Exception as e:
                        print(f"Error generating plot {plot_name}: {e}")
                        axes[row, col].text(0.5, 0.5, 'Error', ha='center', va='center', fontsize=12, color='red')
                        axes[row, col].set_axis_off()
            else:
                try:
                    plot = plot_function(algorithm_execution_instance, show=False)
                    if plot:
                        plot.canvas.draw()
                        img = plot.canvas.buffer_rgba()
                        axes[row, col].imshow(img)
                        axes[row, col].set_axis_off()
                        plt.close(plot)
                except Exception as e:
                    print(f"Error generating plot {plot_name}: {e}")
                    axes[row, col].text(0.5, 0.5, 'Error', ha='center', va='center', fontsize=12, color='red')
                    axes[row, col].set_axis_off()
        
        return fig
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# Main plotting function
def plot_files_in_directory(directory_path, selected_files="all", selected_plots=list(PLOT_METHODS.keys()), timeout=60):
    pdf_path = os.path.join(directory_path, 'custom_plots_comparison.pdf')
    all_files = [file for file in os.listdir(directory_path) if file.endswith(".txt")]
    
    if selected_files == "all":
        log_files = all_files
    else:
        log_files = [file for file in all_files if file in selected_files]
    
    if not log_files:
        print("No files to process.")
        return
    
    with PdfPages(pdf_path) as pdf:
        for file in log_files:
            file_path = os.path.join(directory_path, file)
            print(f"Now plotting {file_path} and saving to {pdf_path}")
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(plot_file, file_path, selected_plots, timeout)
                try:
                    fig = future.result(timeout=timeout)
                    if fig:
                        pdf.savefig(fig)
                        plt.close(fig)
                except FuturesTimeoutError:
                    print(f"File {file} took too long to generate.")
                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    ax.text(0.5, 0.5, f"Error: {file}\ntook too long to generate", ha='center', va='center', fontsize=12, color='red')
                    ax.set_axis_off()
                    pdf.savefig(fig)
                    plt.close(fig)

# Example usage
if __name__ == "__main__":
    # Directory containing log files
    directory = r"C:\Users\Julian Seminar\Desktop\Examples for paper"
    
    # Specify files (use "all" for all files)
    files_to_plot = "all"
    
    # Specify plots (use list of plot names from PLOT_METHODS.keys())
    plots_to_include = [
        "New_Individuals_Per_Population_Plot",
        "FinalTestsFoundPerIterationPlot"
    ]
    
    # Call the function
    plot_files_in_directory(directory, selected_files=files_to_plot, selected_plots=plots_to_include)
