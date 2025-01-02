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
from src.Visualizations.Plots.New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from src.Visualizations.Plots.FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from src.Visualizations.Plots.FrontPlots import FrontPlots
from src.Visualizations.Plots.NewGoalsPerIterationPlot import NewGoalsPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot_different_calculation import Goals_per_Iteration_Plot_different_calculation
from src.Visualizations.Plots.GoalsIntersectionPlot import GoalsIntersectionPlot
from src.Visualizations.Plots.AdditionOfNewGoalsPlot import AdditionOfNewGoalsPlot

class VisualizationBase:
    """Abstract base class defining the interface for DynaMOSA visualization strategies."""
    
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

    def create_plot(self, plot_name: str, algorithm_execution_instance: algorithm_execution) -> Optional[plt.Figure]:
        """
        Create a visualization of specified metrics from algorithm execution data.

        Args:
            plot_name: Identifier for the desired plot type
            algorithm_execution_instance: Parsed algorithm execution data

        Returns:
            Optional[plt.Figure]: Generated visualization or None if creation fails
        """
        if plot_name not in self.AVAILABLE_PLOTS:
            print(f"Warning: Plot type '{plot_name}' not recognized")
            return None
        
        plot_class, plot_method = self.AVAILABLE_PLOTS[plot_name]
        try:
            plot_instance = plot_class(algorithm_execution_instance)
            plot_method_func = getattr(plot_instance, plot_method)
            return plot_method_func(show=False)
        except Exception as e:
            print(f"Error creating plot {plot_name}: {str(e)}")
            return None

    def process_file(self, file_path: str, selected_plots: List[str], pdf: PdfPages, timeout: int, max_workers: int) -> bool:
        """
        Process algorithm execution data from a single file.

        Args:
            file_path: Path to execution log file
            selected_plots: Types of plots to generate
            pdf: PDF document for plot storage
            timeout: Maximum time allowed for plot generation
            max_workers: Maximum number of concurrent workers

        Returns:
            bool: Success status of file processing
        """
        raise NotImplementedError("Visualization strategy must implement process_file")

    def generate_visualizations(self, directory_path: str, 
                              output_dir: str,                    # New parameter
                              files: Optional[List[str]] = None, 
                              plots: Optional[List[str]] = None, 
                              timeout: int = 60,
                              output_filename: str = 'algorithm_analysis.pdf',
                              max_workers: int = 1) -> None:
        """
        Generate visualizations for algorithm execution data.

        Args:
            directory_path: Location of execution log files
            output_dir: Directory where output files will be saved
            files: Specific files to analyze or None for all files
            plots: Specific metrics to visualize or None for all metrics
            timeout: Maximum time per plot in seconds
            output_filename: Target PDF filename
            max_workers: Maximum number of concurrent workers for plot generation
        """
        if not os.path.exists(directory_path):
            print(f"Input directory not found: {directory_path}")
            return

        if not os.path.exists(output_dir):
            print(f"Output directory not found: {output_dir}")
            return

        if not plots:
            plots = list(self.AVAILABLE_PLOTS.keys())
        else:
            # Validate plot names
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
