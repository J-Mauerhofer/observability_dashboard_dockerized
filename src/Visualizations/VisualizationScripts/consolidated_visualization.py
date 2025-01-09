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
            rows = (num_plots + 3) // 4  # Changed to 4 columns
            
            fig, axes = plt.subplots(rows, 4, figsize=(40, 8 * rows))  # Width increased for 4 columns
            
            if rows == 1:
                axes = axes.reshape(1, -1)
                
            plt.subplots_adjust(
                left=0.05,
                right=0.95,
                bottom=0.05,
                top=0.95,
                wspace=0.15,
                hspace=0.2
            )

            fig.suptitle(f"Analysis of {algorithm_execution_instance.name}", 
                        fontsize=35, y=0.98, weight='bold')

            success = True
            plot_results = queue.Queue()

            def create_and_queue_plot(plot_name: str, row: int, col: int) -> None:
                try:
                    plot_fig = self.create_plot(plot_name, algorithm_execution_instance)
                    if plot_fig:
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
                    row, col = divmod(idx, 4)  # Changed to 4 columns
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
            for idx in range(len(selected_plots), rows * 4):  # Changed to 4 columns
                row, col = divmod(idx, 4)  # Changed to 4 columns
                axes[row, col].set_visible(False)

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