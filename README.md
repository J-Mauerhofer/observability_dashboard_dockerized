# Observability Dashboard for EvoSuite

## Overview
The Observability Dashboard for EvoSuite is a visualization tool that provides insights into the runtime behavior of EvoSuite's test generation process. It consists of two main components:

- **Log generation utility**: Interfaces with a modified version of EvoSuite to produce detailed execution logs.
- **Visualization dashboard**: Transforms these logs into meaningful visualizations.

[Paper Citation - TBD]  
[Authors - TBD]  
[Institution - TBD]

---

## Prerequisites

- **Python** (recent version recommended)

### For log generation:
- **Linux operating system**
- **Java 8**
- Modified version of EvoSuite (available at [GitHub Repository](https://github.com/DominikFischli/evosuite.git))
- EvoSuite runtime test dependency

---

## Installation

```bash
git clone https://github.com/J-Mauerhofer/LogFileVisualizer.git
cd [repository-name]
pip install -r requirements.txt
```

---

## Usage

### Generating Logs

1. Ensure you have a compiled Java 8 project.
2. Configure your log generation settings in `scripts/log_generation/config.json`.
3. Run the log generation script (must be on Linux):

   ```bash
   python scripts/log_generation/generate_logs.py
   ```

### Creating Visualizations

1. Place your log files in a dedicated directory.
2. Specify said directory in the visualization_config.json file in `scripts/visualization/visualization_config.json`.
3. Run the visualization script:

   ```bash
   python scripts/visualization/run_visualization.py
   ```

---

## Available Visualizations

1. **New Individuals View**  
   Tracks the number of newly generated test cases per iteration, providing insights into the progress of test generation.

2. **Final Tests View**  
   Shows which iterations contributed tests to the final test suite, helping identify productive phases of the generation process.

3. **Goals Progress View**  
   Displays four charts tracking:
   - Uncovered goals
   - Covered goals
   - Current goals
   - Total goals

   This view helps understand DynaMOSA's goal management behavior.

4. **Detailed Fronts View**  
   A stacked area chart showing the distribution of individuals across different fronts in each iteration, with each population containing exactly 50 individuals.

5. **Simple Fronts View**  
   A simplified version of the fronts visualization, showing only the number of fronts per iteration.

6. **New Goals View**  
   Tracks the introduction of new current goals across iterations, helping understand how the goal set evolves.

---

## Example Data
Example log files are provided in the `example_logs` directory to help you get started.