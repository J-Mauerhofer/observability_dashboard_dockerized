#!/usr/bin/env python3

import os
import subprocess
import json
from datetime import datetime
import sys

def load_config(config_path):
    """Load the JSON configuration file."""
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Configuration file '{config_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing the configuration file: {e}")
        sys.exit(1)

def create_logs_directory(base_dir):
    """Create 'enhanced_logs' directory if it doesn't exist."""
    logs_dir = os.path.join(base_dir, "enhanced_logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir

def resolve_path(path, base_dir):
    """Resolve the given path to an absolute path."""
    if os.path.isabs(path):
        return path
    return os.path.abspath(os.path.join(base_dir, path))

def validate_class_names(classes):
    """Ensure class names are fully qualified."""
    for class_name in classes:
        if '.' not in class_name:
            print(f"Invalid class name '{class_name}'. Class names must be fully qualified (e.g., 'com.example.MyClass').")
            sys.exit(1)

def run_evosuite(class_name, project_cp, seed, jar_path, logs_dir):
    """Execute EvoSuite for a single class and save logs."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Starting test generation for class: {class_name}")

    # Construct the EvoSuite command
    command = [
        "java",
        "-jar",
        jar_path,
        "-class",
        class_name,
        "-projectCP",
        project_cp,
        "-seed",
        str(seed)
    ]

    try:
        # Execute the command and capture the output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Define the log file path
        class_simple_name = class_name.split('.')[-1]
        log_file_path = os.path.join(logs_dir, f"{class_simple_name}_logs.txt")

        # Write the output to the log file
        with open(log_file_path, 'w') as log_file:
            log_file.write(result.stdout)

        # Check if EvoSuite executed successfully
        if result.returncode == 0:
            print(f"Completed {class_simple_name}. Logs saved to {log_file_path}\n")
        else:
            print(f"EvoSuite encountered an error for {class_simple_name}. Check {log_file_path} for details.\n")

    except Exception as e:
        print(f"An error occurred while running EvoSuite for {class_name}: {e}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 evosuite_runner.py <path_to_config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)

    classes = config.get('classes_under_test', [])
    classpath_config = config.get('classpath', '')
    seed = config.get('seed', 0)
    jar_path_config = config.get('jar_path', '')
    base_dir_config = config.get('base_directory', '')

    if not all([classes, classpath_config, jar_path_config, base_dir_config]):
        print("Please ensure all configuration fields are properly set.")
        sys.exit(1)

    # Validate class names
    validate_class_names(classes)

    # Resolve base directory to absolute path
    base_dir = resolve_path(base_dir_config, os.getcwd())

    # Resolve classpath relative to base_directory
    project_cp = resolve_path(classpath_config, base_dir)

    # Resolve jar_path relative to base_directory (if not absolute)
    jar_path = resolve_path(jar_path_config, base_dir)

    # Verify that jar_path exists
    if not os.path.isfile(jar_path):
        print(f"The specified jar_path does not exist: {jar_path}")
        sys.exit(1)

    # Verify that classpath exists
    if not os.path.exists(project_cp):
        print(f"The specified classpath does not exist: {project_cp}")
        sys.exit(1)

    logs_dir = create_logs_directory(base_dir)

    total_classes = len(classes)
    for index, class_name in enumerate(classes, start=1):
        run_evosuite(class_name, project_cp, seed, jar_path, logs_dir)
        print(f"Progress: {index}/{total_classes} classes completed.\n")

    print("All test generations completed.")

if __name__ == "__main__":
    main()
