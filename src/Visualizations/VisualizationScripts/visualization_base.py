# visualization_base.py
"""
The other visualization classes inherit from this class.
"""

import matplotlib
matplotlib.use('Agg')  # Must be called before any other matplotlib imports

import os
import sys
from typing import List, Optional, Dict, Type
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# Add the project base directory to sys.path if not already present
project_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_base_dir not in sys.path:
    sys.path.insert(0, project_base_dir)

from src.DynaMOSA_Model.algorithm_execution import algorithm_execution
from src.Visualizations.Plots.NewIndividualsView import NewIndividualsView
from src.Visualizations.Plots.FinalTetsView import FinalTestsView
from src.Visualizations.Plots.GoalsProgressView import GoalsProgressView
from src.Visualizations.Plots.FrontsView import FrontsView
from src.Visualizations.Plots.NewCurrentGoalsView import NewCurrentGoalsView
from src.Visualizations.Plots.CoveredAndUncoveredGoalsView import CoveredAndUncoveredGoalsView
from src.Visualizations.Plots.NonInitialGoalsView import NonInitialGoalsView
from src.Visualizations.Plots.AverageCrowdingDistanceView import AverageCrowdingDistanceView
from src.Visualizations.Plots.AverageFitnessView import AverageFitnessView

class VisualizationBase:
    """Abstract base class defining the interface for DynaMOSA visualization strategies."""
    
    AVAILABLE_PLOTS = {
        'new_individuals': (NewIndividualsView, 'plot_number_of_individuals_not_present_in_last_population_per_population'),
        'final_tests': (FinalTestsView, 'plot_number_of_final_tests_generated_per_iteration'),
        'goals_per_iteration': (GoalsProgressView, 'plot_goals_per_iteration'),
        'front_sizes': (FrontsView, 'plot_front_sizes_in_stacked_area_chart'),
        'front_numbers': (FrontsView, 'plot_number_of_fronts_per_population'),
        'new_goals': (NewCurrentGoalsView, 'plot_number_of_new_goals_per_iteration'),
        'goals_intersection': (CoveredAndUncoveredGoalsView, 'plot_goals_intersection'),
        'additional_goals': (NonInitialGoalsView, 'plot_number_of_goals_not_among_initial_goals'),
        'average_crowding_distance': (AverageCrowdingDistanceView, 'plot_average_crowding_distance'),
        'average_fitness': (AverageFitnessView, 'plot_average_fitness')
    }

    def create_plot(self, plot_name: str, algorithm_execution_instance: algorithm_execution, title_size: int = 22) -> Optional[plt.Figure]:
        """
        Create a visualization of specified metrics from algorithm execution data.
        
        Args:
            plot_name: Identifier for the desired plot type
            algorithm_execution_instance: Parsed algorithm execution data
            title_size: Size of the plot title (default: 14)
        """
        if plot_name not in self.AVAILABLE_PLOTS:
            print(f"Warning: Plot type '{plot_name}' not recognized")
            return None
        
        plot_class, plot_method = self.AVAILABLE_PLOTS[plot_name]
        try:
            plot_instance = plot_class(algorithm_execution_instance)
            plot_method_func = getattr(plot_instance, plot_method)
            # Pass title_size if the method accepts it
            import inspect
            if 'title_size' in inspect.signature(plot_method_func).parameters:
                return plot_method_func(show=False, title_size=title_size)
            return plot_method_func(show=False)
        except Exception as e:
            print(f"Error creating plot {plot_name}: {str(e)}")
            return None

    def process_file(self, file_path: str, selected_plots: List[str], pdf: PdfPages, timeout: int, max_workers: int) -> bool:
        """Process algorithm execution data from a single file."""
        raise NotImplementedError("Visualization strategy must implement process_file")

    def generate_visualizations(self, directory_path: str, 
                              output_dir: str,
                              files: Optional[List[str]] = None, 
                              plots: Optional[List[str]] = None, 
                              timeout: int = 60,
                              output_filename: str = 'algorithm_analysis.pdf',
                              max_workers: int = 1) -> None:
        """Generate visualizations for algorithm execution data."""
        if not os.path.exists(directory_path):
            print(f"Input directory not found: {directory_path}")
            return

        if not os.path.exists(output_dir):
            print(f"Output directory not found: {output_dir}")
            return

        if not plots:
            plots = list(self.AVAILABLE_PLOTS.keys())
        else:
            invalid_plots = [p for p in plots if p not in self.AVAILABLE_PLOTS]
            if invalid_plots:
                print(f"Warning: Invalid plot types: {invalid_plots}")
                plots = [p for p in plots if p in self.AVAILABLE_PLOTS]

            if not plots:
                print("No valid plots selected for generation")
                return

        if files and files != ['all']:
            log_files = [f for f in files if f.endswith('.txt') and 
                        os.path.exists(os.path.join(directory_path, f))]
        else:
            log_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

        if not log_files:
            print(f"No valid log files found in {directory_path}")
            return

        pdf_path = os.path.join(output_dir, output_filename)
        failed_files = []

        with PdfPages(pdf_path) as pdf:
            # Add metadata to PDF
            d = pdf.infodict()
            d['Title'] = 'DynaMOSA Algorithm Analysis'
            d['Author'] = 'DynaMOSA Visualization Tool'
            d['Subject'] = 'Algorithm Execution Analysis'
            d['Keywords'] = 'DynaMOSA, testing, analysis'
            
            for file in log_files:
                file_path = os.path.join(directory_path, file)
                print(f"Processing {file_path}")
                
                if not self.process_file(file_path, plots, pdf, timeout, max_workers):
                    failed_files.append(file)

        if failed_files:
            print("\nFailed to process files:")
            for file in failed_files:
                print(f"- {file}")

# consolidated_visualization.py
"""
This visualization script will place all plots for a single class on a single page.
"""

import matplotlib
matplotlib.use('Agg')  # Must be called before any other matplotlib imports

import matplotlib.pyplot as plt
from typing import List, Tuple
from matplotlib.backends.backend_pdf import PdfPages
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import queue

from src.DynaMOSA_Model.algorithm_execution import algorithm_execution
from src.Visualizations.VisualizationScripts.visualization_base import VisualizationBase

class ConsolidatedVisualization(VisualizationBase):
    """Visualization strategy that combines multiple metrics on a single page."""

    def process_file(self, file_path: str, selected_plots: List[str], pdf: PdfPages, timeout: int, max_workers: int) -> bool:
        """Generate consolidated visualization of multiple metrics."""
        if not selected_plots:
            print("No plots selected for generation")
            return False

        try:
            algorithm_execution_instance = algorithm_execution(file_path)
            num_plots = len(selected_plots)
            rows = (num_plots + 2) // 3
            
            # Reduced figure height and tighter spacing
            fig, axes = plt.subplots(rows, 3, figsize=(30, 8 * rows))
            
            if rows == 1:
                axes = axes.reshape(1, -1)
                
            # Adjust spacing between subplots
            plt.subplots_adjust(
                left=0.05,    # Reduced left margin
                right=0.95,   # Reduced right margin
                bottom=0.05,  # Reduced bottom margin
                top=0.95,     # Reduced top margin
                wspace=0.15,  # Reduced horizontal space between plots
                hspace=0.2    # Reduced vertical space between plots
            )

            # Move title closer to plots and make it more compact
            fig.suptitle(f"Analysis of {algorithm_execution_instance.name}", 
                        fontsize=22, y=0.98, weight='bold')

            success = True
            plot_results = queue.Queue()

            def create_and_queue_plot(plot_name: str, row: int, col: int) -> None:
                """Helper function to create plot and queue results"""
                try:
                    plot_fig = self.create_plot(plot_name, algorithm_execution_instance, title_size=22)
                    if plot_fig:
                        # Make individual plot more compact
                        plot_fig.tight_layout(pad=0.1)
                        plot_fig.canvas.draw()
                        img = plot_fig.canvas.buffer_rgba()
                        plot_results.put((row, col, img, None, plot_fig))
                    else:
                        plot_results.put((row, col, None, f'Failed to generate: {plot_name}', None))
                except Exception as e:
                    plot_results.put((row, col, None, str(e), None))

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for idx, plot_name in enumerate(selected_plots):
                    row, col = divmod(idx, 3)
                    future = executor.submit(create_and_queue_plot, plot_name, row, col)
                    futures.append((future, plot_name, row, col))

                for future, plot_name, row, col in futures:
                    try:
                        future.result(timeout=timeout)
                    except TimeoutError:
                        success = False
                        plot_results.put((row, col, None, f"Timeout generating {plot_name}", None))
                    except Exception as e:
                        success = False
                        plot_results.put((row, col, None, f"Error generating {plot_name}: {str(e)}", None))

            while not plot_results.empty():
                row, col, img, error, plot_fig = plot_results.get()
                if img is not None:
                    axes[row, col].imshow(img)
                    axes[row, col].set_axis_off()
                    if plot_fig:
                        plt.close(plot_fig)
                else:
                    success = False
                    axes[row, col].text(0.5, 0.5, error,
                                      ha='center', va='center',
                                      fontsize=10, color='red')
                    axes[row, col].set_axis_off()

            # Hide unused subplots
            for idx in range(len(selected_plots), rows * 3):
                row, col = divmod(idx, 3)
                axes[row, col].set_visible(False)

            # Apply tight layout to the entire figure
            fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
            
            pdf.savefig(fig, bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)
            return success

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False

if __name__ == "__main__":
    visualizer = ConsolidatedVisualization()
    visualizer.generate_visualizations(
        directory_path="path/to/execution/logs",
        output_filename="consolidated_analysis.pdf"
    )