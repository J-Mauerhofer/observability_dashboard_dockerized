import sys
import os

# Add the project base directory to sys.path
project_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_base_dir)

# Save this as example_usage.py
from src.Visualizations.PlottingScripts.plots_on_same_page2 import generate_plots



# Example 3: Generate all plots for specific files with longer timeout
generate_plots(
    directory_path=r"C:\Users\Julian Seminar\Desktop\Examples for paper",
    files=['logFilede.outstare.fortbattleplayer.gui.battlefield.BattlefieldCell.txt', 'logFilede.outstare.fortbattleplayer.player.actions.HitAction.txt'],
    timeout=120
)