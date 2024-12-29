import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import sys
from typing import List, Optional, Dict, Type

# Add the project base directory to sys.path
project_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_base_dir)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from src.DynaMOSA_Model.algorithm_execution import algorithm_execution

# Import all plot classes
from src.Visualizations.Plots.New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from src.Visualizations.Plots.FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from src.Visualizations.Plots.FrontPlots import FrontPlots
from src.Visualizations.Plots.NewGoalsPerIterationPlot import NewGoalsPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot_different_calculation import Goals_per_Iteration_Plot_different_calculation
from src.Visualizations.Plots.GoalsIntersectionPlot import GoalsIntersectionPlot
from src.Visualizations.Plots.AdditionOfNewGoalsPlot import AdditionOfNewGoalsPlot

# Dictionary mapping plot names to their classes and methods
AVAILABLE_PLOTS = {
    'new_individuals': (New_Individuals_Per_Population_Plot, 'plot_number_of_individuals_not_present_in_last_population_per_population'),
    'final_tests': (FinalTestsFoundPerIterationPlot, 'plot_number_of_final_tests_generated_per_iteration'),
    'goals_per_iteration': (Goals_per_Iteration_Plot, 'plot_goals_per_iteration'),
    'goals_different_calc': (Goals_per_Iteration_Plot_different_calculation, 'plot_goals_per_iteration'),
    'goals_intersection': (GoalsIntersectionPlot, 'plot_goals_intersection'),
    'front_sizes': (FrontPlots, 'plot_front_sizes_in_stacked_area_chart'),
    'front_numbers': (FrontPlots, 'plot_number_of_fronts_per_population'),
    'new_goals': (NewGoalsPerIterationPlot, 'plot_number_of_new_goals_per_iteration'),
    'additional_goals': (AdditionOfNewGoalsPlot, 'plot_number_of_goals_not_among_initial_goals')
}

def create_plot(plot_name: str, algorithm_execution_instance: algorithm_execution) -> Optional[plt.Figure]:
    """
    Creates a single visualization plot based on the given plot name.

    Args:
        plot_name (str): Name of the plot to create (must be one of AVAILABLE_PLOTS)
        algorithm_execution_instance (algorithm_execution): Instance containing the data to plot

    Returns:
        Optional[plt.Figure]: Matplotlib figure if successful, None if plot creation fails
    """

    if plot_name not in AVAILABLE_PLOTS:
        print(f"Warning: Plot type '{plot_name}' not recognized")
        return None
    
    plot_class, plot_method = AVAILABLE_PLOTS[plot_name]
    try:
        plot_instance = plot_class(algorithm_execution_instance)
        plot_method_func = getattr(plot_instance, plot_method)
        return plot_method_func(show=False)
    except Exception as e:
        print(f"Error creating plot {plot_name}: {e}")
        return None

def plot_file(file_path: str, selected_plots: List[str], timeout: int = 60) -> Optional[plt.Figure]:
    """
    Creates a figure containing multiple plots for a single log file.

    Args:
        file_path (str): Path to the log file to process
        selected_plots (List[str]): List of plot names to generate
        timeout (int, optional): Maximum time in seconds to process the file. Defaults to 60

    Returns:
        Optional[plt.Figure]: Combined figure with all plots if successful, None if processing fails
    """
    try:
        algorithm_execution_instance = algorithm_execution(file_path)
        num_plots = len(selected_plots)
        rows = (num_plots + 2) // 3  # Calculate needed rows (3 plots per row)
        fig, axes = plt.subplots(rows, 3, figsize=(30, 10 * rows))
        if rows == 1:
            axes = axes.reshape(1, -1)
        plt.subplots_adjust(wspace=0.05, hspace=0.01)

        # Add main title to the figure with larger font size
        fig.suptitle(f"Analysis for {algorithm_execution_instance.name}", 
                    fontsize=24, y=0.98, weight='bold')

        for idx, plot_name in enumerate(selected_plots):
            row, col = divmod(idx, 3)
            plot_fig = create_plot(plot_name, algorithm_execution_instance)
            
            if plot_fig:
                plot_fig.canvas.draw()
                img = plot_fig.canvas.buffer_rgba()
                axes[row, col].imshow(img)
                axes[row, col].set_axis_off()
                plt.close(plot_fig)
            else:
                axes[row, col].text(0.5, 0.5, f'Error: Plot {plot_name} not generated',
                                  ha='center', va='center', fontsize=12, color='red')
                axes[row, col].set_axis_off()

        # Hide empty subplots
        for idx in range(len(selected_plots), rows * 3):
            row, col = divmod(idx, 3)
            axes[row, col].set_visible(False)

        return fig
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

    
def generate_plots(
    directory_path: str,
    files: Optional[List[str]] = None,
    plots: Optional[List[str]] = None,
    timeout: int = 60,
    output_filename: str = 'plots_comparison.pdf'
) -> None:
    """
    Generates visualization plots from log files and saves them to a PDF.

    This is the main function for generating plots from EvoSuite log files. It processes
    the specified files and creates selected visualizations in a combined PDF output.

    Args:
        directory_path (str): Path to the directory containing log files
        files (List[str], optional): Specific files to process. Use None or ['all'] for all .txt files
        plots (List[str], optional): Specific plots to generate. Use None for all available plots
        timeout (int, optional): Maximum time in seconds to process each file. Defaults to 60
        output_filename (str, optional): Name of the output PDF file. Defaults to 'plots_comparison.pdf'

    Available plot types:
        - 'new_individuals': New individuals per population
        - 'final_tests': Final tests found per iteration
        - 'goals_per_iteration': Goals per iteration
        - 'goals_different_calc': Goals per iteration (different calculation)
        - 'goals_intersection': Goals intersection
        - 'front_sizes': Front sizes in stacked area chart
        - 'front_numbers': Number of fronts per population
        - 'new_goals': New goals per iteration
        - 'additional_goals': Additional goals not among initial goals

    Note:
        If processing a file takes longer than the specified timeout,
        it will be listed in the console output as a file that took too long to process.
    """

    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return

    # If no plots are specified, use all available plots
    if not plots:
        plots = list(AVAILABLE_PLOTS.keys())
    else:
        # Validate plot names
        invalid_plots = [p for p in plots if p not in AVAILABLE_PLOTS]
        if invalid_plots:
            print(f"Warning: Invalid plot types: {invalid_plots}")
            plots = [p for p in plots if p in AVAILABLE_PLOTS]

    # Get list of files to process
    if files and files != ['all']:
        log_files = [f for f in files if f.endswith('.txt') and os.path.exists(os.path.join(directory_path, f))]
    else:
        log_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

    if not log_files:
        print(f"No valid log files found in {directory_path}")
        return

    pdf_path = os.path.join(directory_path, output_filename)
    too_large_files = []

    with PdfPages(pdf_path) as pdf:
        for file in log_files:
            file_path = os.path.join(directory_path, file)
            print(f"Now plotting {file_path}")
            
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(plot_file, file_path, plots, timeout)
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

    if too_large_files:
        print("\nFiles that took too long to process:")
        for file in too_large_files:
            print(f"- {file}")