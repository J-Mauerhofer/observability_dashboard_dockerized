import argparse
import json
import os
import sys
from datetime import datetime

# Add the project base directory to sys.path
project_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_base_dir)

from src.Visualizations.VisualizationScripts.sequential_visualization import SequentialVisualization
from src.Visualizations.VisualizationScripts.consolidated_visualization import ConsolidatedVisualization

# Centralized default values
DEFAULTS = {
    "output_filename": "visualization.pdf",
    "plots": "all",
    "strategy": "consolidated",
    "max_workers": 1,
    "timeout": 60,
    "default_config_path": os.path.join(os.path.dirname(__file__), "visualization_config.json")
}

# Available visualization strategies
STRATEGIES = {
    "sequential": SequentialVisualization,
    "consolidated": ConsolidatedVisualization,
}

# Dynamically fetch available plots from the VisualizationBase class
from src.Visualizations.VisualizationScripts.visualization_base import VisualizationBase
AVAILABLE_PLOTS = list(VisualizationBase.AVAILABLE_PLOTS.keys())

def load_config(config_path):
    """Load the configuration from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def get_unique_filename(directory, filename):
    """Generate a unique filename by appending a timestamp, and fallback to incremental numbering if necessary."""
    base, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    unique_filename = f"{base}-{timestamp}{ext}"

    # Check if the timestamped filename is already unique
    if not os.path.exists(os.path.join(directory, unique_filename)):
        return unique_filename

    # Fallback to incremental numbering if needed
    counter = 1
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base}-{counter}{ext}"
        counter += 1
    return unique_filename

def print_help():
    """Print detailed help for using the script."""
    print(f"""
    Usage: python run_visualizations.py [OPTIONS]

    This script generates visualizations for EvoSuite logs. The visualizations can be configured
    through command-line arguments or a configuration file. Missing arguments are resolved
    from the configuration file or default values.

    Required:
      --input_directory      Absolute path to the directory containing log files. If specified in the
                             configuration file, this argument is not mandatory.

    Optional:
      --output_directory     Absolute path to save output files. If not provided, a folder named
                             'visualization' will be created in the input directory.
      --output_filename      Name of the output PDF file. If not provided, defaults to 'visualization.pdf'.
      --plots                Comma-separated list of plots to generate, or 'all' for all plots.
                             Available plots: {', '.join(AVAILABLE_PLOTS)}
      --strategy             Visualization strategy to use ('sequential' or 'consolidated').
      --max_workers          Maximum number of threads for parallel processing.
      --timeout              Timeout per plot in seconds.
      --config               Path to the configuration file. Use 'default' to load the default
                             configuration from {DEFAULTS['default_config_path']}.

    Examples:
      1. Minimal command:
         python run_visualizations.py --input_directory /path/to/logs

      2. Specify output directory:
         python run_visualizations.py --input_directory /path/to/logs --output_directory /path/to/output

      3. Use default configuration file:
         python run_visualizations.py --config default

      4. Generate all plots with a custom output filename:
         python run_visualizations.py --input_directory /path/to/logs --output_filename custom.pdf --plots all

    """)

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Run visualizations for EvoSuite logs.", add_help=False)
    parser.add_argument("--input_directory", type=str, help="Absolute path to the directory containing log files.")
    parser.add_argument("--output_directory", type=str, help="Absolute path to the directory for saving output files. If not provided, a 'visualization' folder will be created in the input directory.")
    parser.add_argument("--output_filename", type=str, help=f"Name of the output PDF (default: {DEFAULTS['output_filename']}).")
    parser.add_argument("--plots", type=str, help=f"Comma-separated list of plots to generate or 'all' for all plots (default: {DEFAULTS['plots']}).")
    parser.add_argument("--strategy", type=str, choices=STRATEGIES.keys(), help=f"Visualization strategy to use (default: {DEFAULTS['strategy']}).")
    parser.add_argument("--max_workers", type=int, help=f"Maximum number of threads for parallel processing (default: {DEFAULTS['max_workers']}).")
    parser.add_argument("--timeout", type=int, help=f"Timeout per plot in seconds (default: {DEFAULTS['timeout']}).")
    parser.add_argument("--config", type=str, help=f"Path to the configuration file or 'default' for default config.")
    parser.add_argument("--help", action="store_true", help="Show this help message and exit.")

    args = parser.parse_args()

    # Show help and exit if --help is provided
    if args.help:
        print_help()
        return

    # Handle configuration file
    config = {}
    if args.config:
        config_path = DEFAULTS["default_config_path"] if args.config == "default" else args.config
        config = load_config(config_path)

    # Resolve parameters
    input_directory = args.input_directory or config.get("input_directory")
    if not input_directory:
        raise ValueError("Error: 'input_directory' must be specified either in the command line or the configuration file.")
    if not os.path.isabs(input_directory):
        raise ValueError("Error: 'input_directory' must be an absolute path.")
    if not os.path.exists(input_directory):
        raise ValueError(f"Error: The specified 'input_directory' does not exist: {input_directory}")

    output_directory = args.output_directory
    if output_directory:
        if not os.path.isabs(output_directory):
            raise ValueError("Error: 'output_directory' must be an absolute path.")
    else:
        # Default behavior: use a 'visualization' folder inside the input directory
        output_directory = os.path.join(input_directory, "visualization")
        os.makedirs(output_directory, exist_ok=True)

    output_filename = args.output_filename or config.get("output_filename", DEFAULTS["output_filename"])

    # Ensure the output filename is unique
    output_filename = get_unique_filename(output_directory, output_filename)

    # Resolve plots: if 'all', use all available plots
    if args.plots == "all" or (not args.plots and config.get("plots") == "all"):
        plots = AVAILABLE_PLOTS
    elif args.plots:
        plots = args.plots.split(",")
    else:
        plots = config.get("plots", DEFAULTS["plots"])
        if plots == "all":
            plots = AVAILABLE_PLOTS

    strategy = args.strategy or config.get("strategy", DEFAULTS["strategy"])
    max_workers = args.max_workers or config.get("max_workers", DEFAULTS["max_workers"])
    timeout = args.timeout or config.get("timeout", DEFAULTS["timeout"])

    # Validate strategy
    if strategy not in STRATEGIES:
        raise ValueError(f"Invalid strategy '{strategy}'. Available options: {list(STRATEGIES.keys())}")

    # Run the visualization
    visualizer_class = STRATEGIES[strategy]
    visualizer = visualizer_class()
    visualizer.generate_visualizations(
        directory_path=input_directory,
        output_dir=output_directory,
        output_filename=output_filename,
        plots=plots,
        timeout=timeout,
        max_workers=max_workers
    )
    print(f"Visualization completed successfully. Results saved in: {os.path.join(output_directory, output_filename)}")

if __name__ == "__main__":
    main()
