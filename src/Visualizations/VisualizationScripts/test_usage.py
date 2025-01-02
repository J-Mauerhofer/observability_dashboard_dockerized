"""visualization_test.py

Test script demonstrating both visualization approaches.
"""
import sys
import os

# Add the project base directory to sys.path
project_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_base_dir)

from src.Visualizations.VisualizationScripts.consolidated_visualization import ConsolidatedVisualization
from src.Visualizations.VisualizationScripts.sequential_visualization import SequentialVisualization

def test_visualizations(directory_path: str):
    """
    Test both visualization approaches with various configurations.
    
    Args:
        directory_path: Path to directory containing log files
    """
    print("Starting visualization tests...\n")

    # Test 1: Consolidated visualization with all plots
    print("Test 1: Consolidated visualization - all plots")
    consolidated_viz = ConsolidatedVisualization()
    consolidated_viz.generate_visualizations(
        directory_path=directory_path,
        output_filename="test_consolidated_all.pdf"
    )
    print("Completed consolidated visualization with all plots\n")

    # Test 2: Sequential visualization with all plots
    print("Test 2: Sequential visualization - all plots")
    sequential_viz = SequentialVisualization()
    sequential_viz.generate_visualizations(
        directory_path=directory_path,
        output_filename="test_sequential_all.pdf"
    )
    print("Completed sequential visualization with all plots\n")

    # Test 3: Consolidated visualization with specific plots
    print("Test 3: Consolidated visualization - selected plots")
    selected_plots = ['new_individuals', 'goals_per_iteration', 'front_sizes']
    consolidated_viz.generate_visualizations(
        directory_path=directory_path,
        plots=selected_plots,
        output_filename="test_consolidated_selected.pdf"
    )
    print("Completed consolidated visualization with selected plots\n")

    # Test 4: Sequential visualization with specific plots
    print("Test 4: Sequential visualization - selected plots")
    sequential_viz.generate_visualizations(
        directory_path=directory_path,
        plots=selected_plots,
        output_filename="test_sequential_selected.pdf"
    )
    print("Completed sequential visualization with selected plots\n")

    # Test 5: Both visualizations with specific files
    specific_files = ['file1.txt', 'file2.txt']  # Replace with actual file names
    print("Test 5: Both visualizations - specific files")
    consolidated_viz.generate_visualizations(
        directory_path=directory_path,
        files=specific_files,
        output_filename="test_consolidated_specific_files.pdf"
    )
    sequential_viz.generate_visualizations(
        directory_path=directory_path,
        files=specific_files,
        output_filename="test_sequential_specific_files.pdf"
    )
    print("Completed visualizations with specific files\n")

    print("All visualization tests completed!")

if __name__ == "__main__":
    # Replace with your log files directory
    log_directory = r"C:\Users\Julian Seminar\Desktop\Examples for paper"
    test_visualizations(log_directory)