#!/usr/bin/env python3
import os
import sys
import json
import shutil
import subprocess
import argparse
from datetime import datetime

# Adjust these paths to point to where you store your custom EvoSuite JAR and runtime locally
CUSTOM_EVOSUITE_JAR_LOCAL_PATH = "PATH_TO_EVOSUITE_JAR/evosuite-X.Y.Z.jar"
STANDALONE_RUNTIME_LOCAL_PATH  = "PATH_TO_EVOSUITE_JAR/evosuite-standalone-runtime-X.Y.Z.jar"

LOG_DIR_NAME = "LogFiles_EvoSuiteLogger"

def copy_if_missing(src, dest):
    """
    Copy file 'src' to 'dest' if and only if 'dest' does not exist.
    """
    if not os.path.isfile(dest):
        shutil.copy(src, dest)

def build_log_filename(class_name=None):
    """
    If a single class name is detected, use logs<ClassName>.txt,
    otherwise use logsMultipleClasses_<timestamp>.txt.
    """
    if class_name:
        # Replace dots with underscores in class name
        clean_name = class_name.replace('.', '_')
        return f"logs{clean_name}.txt"
    else:
        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"logsMultipleClasses_{time_str}.txt"

def run_evosuite(command_args, log_path):
    """
    Run EvoSuite with the given command_args, capture stdout+stderr,
    and store them in log_path.
    """
    with open(log_path, "w", encoding="utf-8") as log_file:
        process = subprocess.Popen(
            command_args,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            shell=False
        )
        process.wait()
        return process.returncode

def handle_no_config_mode(unknown_args):
    """
    Handle the mode where user passes:
      python EvosuiteLogger.py /absolute/path/to/projectRoot [EvoSuite args...]
    """
    if len(unknown_args) < 1:
        print("[ERROR] You must provide the absolute path to the project root.")
        sys.exit(1)

    project_root = unknown_args[0]
    if not os.path.isabs(project_root):
        print(f"[ERROR] The project root must be an absolute path: {project_root}")
        sys.exit(1)

    # The rest are the EvoSuite parameters
    evosuite_args = unknown_args[1:]

    # Move to the project root
    os.chdir(project_root)

    # Copy JAR and runtime if missing
    evosuite_jar_name = os.path.basename(CUSTOM_EVOSUITE_JAR_LOCAL_PATH)
    standalone_name   = os.path.basename(STANDALONE_RUNTIME_LOCAL_PATH)
    copy_if_missing(CUSTOM_EVOSUITE_JAR_LOCAL_PATH, evosuite_jar_name)
    copy_if_missing(STANDALONE_RUNTIME_LOCAL_PATH,  standalone_name)

    # Create log directory if missing
    os.makedirs(LOG_DIR_NAME, exist_ok=True)

    # Attempt to detect a single class name from the arguments, if present
    class_name = None
    if "-class" in evosuite_args:
        try:
            idx = evosuite_args.index("-class")
            class_name = evosuite_args[idx+1]
        except (IndexError, ValueError):
            pass

    # Build log file name
    log_file_name = build_log_filename(class_name)
    log_file_path = os.path.join(LOG_DIR_NAME, log_file_name)

    # Construct the full command
    # Example: java -jar evosuite.jar [evosuite_args...]
    command = ["java", "-jar", evosuite_jar_name] + evosuite_args

    print(f"[INFO] Running EvoSuite with arguments: {' '.join(evosuite_args)}")
    print(f"[INFO] Log will be saved to: {log_file_path}")

    return_code = run_evosuite(command, log_file_path)

    if return_code == 0:
        print("[INFO] EvoSuite run completed successfully.")
    else:
        print(f"[WARNING] EvoSuite run exited with non-zero status: {return_code}")

def handle_config_mode(config_file):
    """
    Handle the mode where user passes:
      python EvosuiteLogger.py --config /absolute/path/to/config.json
    """
    if not os.path.isabs(config_file):
        print(f"[ERROR] The config path must be absolute: {config_file}")
        sys.exit(1)

    # Parse the JSON
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read or parse config file: {e}")
        sys.exit(1)

    # Retrieve project root
    project_root = config.get("projectRoot")
    if not project_root or not os.path.isabs(project_root):
        print("[ERROR] 'projectRoot' must be specified in config and be an absolute path.")
        sys.exit(1)

    # Move to project root
    os.chdir(project_root)

    # Copy JAR and runtime if missing
    evosuite_jar_name = os.path.basename(CUSTOM_EVOSUITE_JAR_LOCAL_PATH)
    standalone_name   = os.path.basename(STANDALONE_RUNTIME_LOCAL_PATH)
    copy_if_missing(CUSTOM_EVOSUITE_JAR_LOCAL_PATH, evosuite_jar_name)
    copy_if_missing(STANDALONE_RUNTIME_LOCAL_PATH,  standalone_name)

    # Create log directory if missing
    os.makedirs(LOG_DIR_NAME, exist_ok=True)

    # We'll also create a "global run log" to document all runs:
    run_log_path = os.path.join(LOG_DIR_NAME, "EvoSuiteLogger_run_log.txt")
    with open(run_log_path, "a", encoding="utf-8") as run_log:
        run_log.write(f"\n===== EvoSuite Logger run at {datetime.now()} =====\n")

        locations   = config.get("locations", [])
        parameters  = config.get("parameters", {})

        for loc in locations:
            # e.g. "target/classes"
            path_entry = loc.get("path", "")
            classes    = loc.get("classes", [])

            # For each class, run EvoSuite
            for cls in classes:
                # Build the command
                # base command: java -jar evosuite.jar -class <cls> -projectCP <path_entry>
                command = [
                    "java",
                    "-jar",
                    evosuite_jar_name,
                    "-class", cls,
                    "-projectCP", path_entry
                ]

                # Append extra parameters from "parameters" dict
                # E.g. {"-criterion": "branch", "-Dsearch_budget": "30"}
                for param_key, param_value in parameters.items():
                    command.append(param_key)
                    command.append(param_value)

                # Prepare log filename
                log_file_name = build_log_filename(cls)
                log_file_path = os.path.join(LOG_DIR_NAME, log_file_name)

                # Run
                run_log.write(f"\n[INFO] Running EvoSuite for class {cls} in {path_entry}\n")
                run_log.write(f"[INFO] Command: {' '.join(command)}\n")

                return_code = run_evosuite(command, log_file_path)
                if return_code == 0:
                    run_log.write(f"[INFO] EvoSuite run for class {cls} completed successfully.\n")
                else:
                    run_log.write(f"[WARNING] EvoSuite run for class {cls} exited with status {return_code}.\n")

        run_log.write("===== End of run =====\n")

def main():
    parser = argparse.ArgumentParser(
        description="Script for running a custom EvoSuite version with logging."
    )
    parser.add_argument(
        "--config", "-c",
        help="Absolute path to the JSON configuration file (for multi-class sequential runs).",
        default=None
    )
    # Capture other arguments in case of no config mode
    known_args, unknown_args = parser.parse_known_args()

    if known_args.config:
        handle_config_mode(known_args.config)
    else:
        handle_no_config_mode(unknown_args)


if __name__ == "__main__":
    main()
