import os
import sys
import json

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, project_root)  # Use insert(0) to prioritize this path

from src.Visualizations.PlottingScripts.PlottingMultipleClassesAndSave import plot_all_executions_in_directories

if __name__ == "__main__":
    # Path to the configuration file
    config_path = os.path.join(current_dir, "visualization_config.json")

    # Check if the configuration file exists
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Load configuration
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Retrieve directories from the configuration
    directories = config.get("directories")
    if not directories or not isinstance(directories, list):
        raise ValueError("The configuration file must contain a 'directories' key with a list of directory paths.")

    # Run the visualization
    plot_all_executions_in_directories(directories)
