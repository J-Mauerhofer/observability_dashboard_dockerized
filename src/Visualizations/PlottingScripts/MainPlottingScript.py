import os
import time  # Import time for tracking elapsed time
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-GUI rendering
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from src.Visualizations.Plots.New_Individuals_Per_Population_Plot import New_Individuals_Per_Population_Plot
from Visualizations.Plots.FinalTestsFoundPerIterationPlot import FinalTestsFoundPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot import Goals_per_Iteration_Plot
from Visualizations.Plots.FrontPlots import FrontPlots
from src.Visualizations.Plots.NewGoalsPerIterationPlot import NewGoalsPerIterationPlot
from src.Visualizations.Plots.Goals_per_Iteration_Plot_different_calculation import Goals_per_Iteration_Plot_different_calculation
from src.Visualizations.Plots.GoalsIntersectionPlot import GoalsIntersectionPlot
from Visualizations.Plots.AdditionOfNewGoalsPlot import AdditionOfNewGoalsPlot
from DynaMOSA_Model.algorithm_execution import algorithm_execution

# Define the size threshold (in kilobytes)
SIZE_THRESHOLD_KB = 500000  # 500,000 KB = ~500 MB

# Function to handle the plotting of a single file
def plot_file(file_path, timeout=60):
    try:
        print(f"Processing file: {file_path}")
        algorithm_execution_instance = algorithm_execution(file_path)
        fig, axes = plt.subplots(3, 3, figsize=(30, 30))  # Create a 3 by 3 grid
        plt.subplots_adjust(wspace=0.05, hspace=0.01)
        plot_class_with_all_plots(algorithm_execution_instance, axes)
        return fig
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# Plot the data for one algorithm execution and save to a PDF
def plot_class_with_all_plots(algorithm_execution_instance, axes):
    figs = []

    try:
        new_individuals_per_population_plot = New_Individuals_Per_Population_Plot(algorithm_execution_instance)
        figs.append(new_individuals_per_population_plot.plot_number_of_individuals_not_present_in_last_population_per_population(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting New_Individuals_Per_Population_Plot: {e}")

    try:
        final_tests_found_per_iteration_plot = FinalTestsFoundPerIterationPlot(algorithm_execution_instance)
        figs.append(final_tests_found_per_iteration_plot.plot_number_of_final_tests_generated_per_iteration(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting FinalTestsFoundPerIterationPlot: {e}")

    try:
        goals_per_iteration_plot = Goals_per_Iteration_Plot(algorithm_execution_instance)
        figs.append(goals_per_iteration_plot.plot_goals_per_iteration(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting Goals_per_Iteration_Plot: {e}")

    try:
        goals_per_iteration_plot_different = Goals_per_Iteration_Plot_different_calculation(algorithm_execution_instance)
        figs.append(goals_per_iteration_plot_different.plot_goals_per_iteration(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting Goals_per_Iteration_Plot_different_calculation: {e}")

    try:
        goals_intersection_plot = GoalsIntersectionPlot(algorithm_execution_instance)
        figs.append(goals_intersection_plot.plot_goals_intersection(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting GoalsIntersectionPlot: {e}")

    try:
        front_plots = FrontPlots(algorithm_execution_instance)
        figs.append(front_plots.plot_front_sizes_in_stacked_area_chart(show=False))
        figs.append(front_plots.plot_number_of_fronts_per_population(show=False))
    except Exception as e:
        figs.extend([None, None])
        print(f"Error plotting FrontPlots: {e}")

    try:
        new_goals_per_iteration_plot = NewGoalsPerIterationPlot(algorithm_execution_instance)
        figs.append(new_goals_per_iteration_plot.plot_number_of_new_goals_per_iteration(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting NewGoalsPerIterationPlot: {e}")

    try:
        addition_of_new_goals_plot = AdditionOfNewGoalsPlot(algorithm_execution_instance)
        figs.append(addition_of_new_goals_plot.plot_number_of_goals_not_among_initial_goals(show=False))
    except Exception as e:
        figs.append(None)
        print(f"Error plotting AdditionOfNewGoalsPlot: {e}")

    for idx, fig in enumerate(figs):
        row, col = divmod(idx, 3)
        if fig:
            fig.canvas.draw()
            img = fig.canvas.buffer_rgba()
            axes[row, col].imshow(img)
            axes[row, col].set_axis_off()
            plt.close(fig)
        else:
            axes[row, col].text(0.5, 0.5, 'Error: Plot not generated', ha='center', va='center', fontsize=12, color='red')
            axes[row, col].set_axis_off()

# Plot the data for all log files in a given directory and save to PDFs
def plot_all_files_in_directory(directory_path, timeout=60, size_threshold_kb=SIZE_THRESHOLD_KB):
    pdf_path = os.path.join(directory_path, 'all_plots_comparison.pdf')
    log_files = [file for file in os.listdir(directory_path) if file.endswith(".txt")]
    total_files = len(log_files)
    start_time = time.time()

    print(f"Found {total_files} .txt files in {directory_path}")

    if not log_files:
        print("No log files found.")
        return

    too_large_files = []  # List to track files that are too large
    skipped_files = []     # List to track files that are skipped due to size

    with PdfPages(pdf_path) as pdf:
        for i, file in enumerate(log_files, start=1):
            file_path = os.path.join(directory_path, file)
            file_size_kb = os.path.getsize(file_path) / 1024  # Size in KB

            if file_size_kb > size_threshold_kb:
                print(f"Skipping file {file} (size: {file_size_kb:.2f} KB) - exceeds threshold of {size_threshold_kb} KB")
                too_large_files.append(file)
                # Optionally, you can create a PDF page indicating the file was skipped
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.text(0.5, 0.5, f"Skipped file:\n{file}\n(Size: {file_size_kb:.2f} KB)", 
                        ha='center', va='center', fontsize=12, color='orange')
                ax.set_axis_off()
                pdf.savefig(fig)
                plt.close(fig)
                continue

            print(f"Now plotting {file_path} and saving to {pdf_path} (size: {file_size_kb:.2f} KB)")
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(plot_file, file_path, timeout)
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
                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    ax.text(0.5, 0.5, f"Error: {file}\ntook too long to generate", 
                            ha='center', va='center', fontsize=12, color='red')
                    ax.set_axis_off()
                    pdf.savefig(fig)
                    plt.close(fig)

            # Calculate progress and time elapsed
            elapsed_time = time.time() - start_time
            progress_percentage = (i / total_files) * 100
            remaining_files = total_files - i

            print("\n\n\n\n###############################################################################################################\n\n\n\n")
            print(f"Progress: {i}/{total_files} ({progress_percentage:.2f}%) | "
                  f"Processed: {i} | Remaining: {remaining_files} | "
                  f"Elapsed Time: {elapsed_time:.2f} seconds")
            print("\n\n\n\n###############################################################################################################\n\n\n\n")

    # If there are large files, generate a second PDF with their names
    if too_large_files:
        larger_pdf_path = os.path.join(directory_path, 'larger_files.pdf')
        with PdfPages(larger_pdf_path) as pdf:
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.text(0.5, 0.95, "Files that were too large to process:", 
                    ha='center', va='top', fontsize=16, weight='bold')
            for i, file in enumerate(too_large_files, start=1):
                ax.text(0.5, 0.95 - i * 0.05, file, ha='center', va='top', fontsize=12)
            ax.set_axis_off()
            pdf.savefig(fig)
            plt.close(fig)

    print(f"Processing completed for directory: {directory_path}")
    if too_large_files:
        print(f"{len(too_large_files)} files were too large and skipped. See 'larger_files.pdf' for details.")

# Plot the data for all log files in the given list of directories and save to PDFs
def plot_all_files_in_directories(directories, timeout=60, size_threshold_kb=SIZE_THRESHOLD_KB):
    for directory in directories:
        print(f"Processing directory: {directory}")
        plot_all_files_in_directory(directory, timeout=timeout, size_threshold_kb=size_threshold_kb)

# List of directories containing log files
directories = [
    #r"C:\Users\Julian Seminar\Desktop\shared ubuntu september24\Log files from automated evosuite runs"
    r"C:\Users\Julian Seminar\Desktop\shared ubuntu september24\Test"

]

# Plot the data and save to PDFs
plot_all_files_in_directories(directories)
