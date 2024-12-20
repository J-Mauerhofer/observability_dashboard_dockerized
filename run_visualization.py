import os
from src.Visualizations.PlottingScripts.PlottingMultipleClassesAndSave import plot_all_executions_in_directories

if __name__ == "__main__":
    # List of directories containing log files
    directories = [
        r"C:\Users\Julian Seminar\Desktop\Examples for paper"
    ]
    
    # Run the visualization
    plot_all_executions_in_directories(directories)