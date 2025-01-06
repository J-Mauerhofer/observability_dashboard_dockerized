# Quick Start Demo

## Prerequisites

Before running the demo, ensure you have the following installed:

* Java 8 JDK
* Apache Maven 3.1 or higher
* Python (recent version)
* Python packages:
  * matplotlib
  * numpy

## Running the Demo

### 1. Set Up the Tutorial Stack Class

Open your terminal and execute the following commands:

```bash
wget http://evosuite.org/files/tutorial/Tutorial_Stack.zip
unzip Tutorial_Stack.zip
cd Tutorial_Stack
mvn compile
```

### 2. Generate Log Files

Open the root directory of this project in a terminal.

Navigate to the log generation scripts directory:

```bash
cd scripts/log_generation
```

Run the EvoSuite Logger (replace the path with your absolute path to the directory Tutorial_Stack):
```bash
python EvosuiteLogger.py "/ABSOLUTE_PATH_TO_TUTORIAL_STACK" -class tutorial.Stack -projectCP target/classes
```

The log file will be generated in Tutorial_Stack/LogFiles_EvoSuiteLogger as logstutorial_Stack.txt.

### 3. Create Visualizations

Navigate to the visualization scripts directory:
```bash
cd ../../scripts/visualization
```

Generate visualizations (replace the path with your absolute path to the directory Tutorial_Stack):
```bash
python EvosuiteVisualizer.py --input_directory "/PATH_TO_TUTORIAL_STACK/LogFiles_EvoSuiteLogger"
```

Now we obtained the visualizations. The visualizations outputs are placed in a the directory Tutorial_Stack/LogFiles_EvoSuiteLogger/visualization.

Here you can see the visualizations (you might get different looking visualizations due to different seeds):
![Visualization Example](visualization_examples/visualization-20250106-010006-1.jpg)