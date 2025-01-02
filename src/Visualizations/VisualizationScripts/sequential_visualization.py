"""
Implementation of sequential visualization strategy that displays each metric
on its own page with supporting context pages.
"""

import matplotlib
matplotlib.use('Agg')  # Must be called before any other matplotlib imports

import matplotlib.pyplot as plt
from typing import List
from matplotlib.backends.backend_pdf import PdfPages
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import queue

from src.DynaMOSA_Model.algorithm_execution import algorithm_execution
from src.Visualizations.VisualizationScripts.visualization_base import VisualizationBase

class SequentialVisualization(VisualizationBase):
    """Visualization strategy that presents metrics sequentially with context pages."""

    def create_title_page(self, class_name: str) -> plt.Figure:
        """
        Create class identification page.

        Args:
            class_name: Name of analyzed class

        Returns:
            plt.Figure: Title page figure
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('off')
        ax.text(0.5, 0.5, f"Analysis of\n{class_name}",
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes,
                fontsize=24,
                fontweight='bold',
                wrap=True)
        return fig

    def create_separator_page(self) -> plt.Figure:
        """
        Create visual separation between class analyses.

        Returns:
            plt.Figure: Separator page figure
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('off')
        return fig

    def process_file(self, file_path: str, selected_plots: List[str], pdf: PdfPages, timeout: int, max_workers: int) -> bool:
        """
        Generate sequential visualization with context pages.

        Args:
            file_path: Path to execution log file
            selected_plots: Types of plots to generate
            pdf: PDF document for plot storage
            timeout: Maximum time allowed for plot generation
            max_workers: Maximum number of concurrent workers

        Returns:
            bool: Success status of file processing
        """
        if not selected_plots:
            print("No plots selected for generation")
            return False

        try:
            algorithm_execution_instance = algorithm_execution(file_path)
            
            # Add title page
            title_page = self.create_title_page(algorithm_execution_instance.name)
            pdf.savefig(title_page)
            plt.close(title_page)

            success = True
            plot_results = queue.Queue()

            def create_and_queue_plot(plot_name):
                try:
                    plot_fig = self.create_plot(plot_name, algorithm_execution_instance)
                    if plot_fig:
                        plot_fig.set_size_inches(12, 8)
                        plot_results.put((plot_name, plot_fig, None))
                    else:
                        plot_results.put((plot_name, None, "Failed to generate plot"))
                except Exception as e:
                    plot_results.put((plot_name, None, str(e)))

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all plot creation tasks
                futures = []
                for plot_name in selected_plots:
                    future = executor.submit(create_and_queue_plot, plot_name)
                    futures.append((future, plot_name))
                
                # Wait for all tasks to complete or timeout
                for future, plot_name in futures:
                    try:
                        future.result(timeout=timeout)
                    except TimeoutError:
                        success = False
                        plot_results.put((plot_name, None, f"Timeout generating {plot_name}"))
                    except Exception as e:
                        success = False
                        plot_results.put((plot_name, None, f"Error generating {plot_name}: {str(e)}"))

            # Process results in order
            while not plot_results.empty():
                plot_name, fig, error = plot_results.get()
                if fig:
                    pdf.savefig(fig)
                    plt.close(fig)
                else:
                    success = False
                    print(f"Error with plot {plot_name}: {error}")

            # Add separator page
            separator_page = self.create_separator_page()
            pdf.savefig(separator_page)
            plt.close(separator_page)

            return success
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False

if __name__ == "__main__":
    visualizer = SequentialVisualization()
    visualizer.generate_visualizations(
        directory_path="path/to/execution/logs",
        output_filename="sequential_analysis.pdf"
    )