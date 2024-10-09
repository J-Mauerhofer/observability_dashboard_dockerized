import os

def copy_first_10_percent(input_path):
    # Check if the input file exists
    if not os.path.exists(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return

    # Generate the output file path
    input_dir = os.path.dirname(input_path)
    input_filename = os.path.basename(input_path)
    output_filename = f"first_10_percent_{input_filename}"
    output_path = os.path.join(input_dir, output_filename)

    # Read the content of the input file
    with open(input_path, 'r') as input_file:
        content = input_file.read()

    # Calculate the length of 1% of the content
    ten_percent_length = len(content) // 400

    # Get the first 10% of the content
    first_ten_percent = content[:ten_percent_length]

    # Write the first 10% to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(first_ten_percent)

    print(f"Successfully copied the first 10% of '{input_path}' to '{output_path}'.")

# Example usage
input_file_path = input("Enter the path of the input file: ")

copy_first_10_percent(input_file_path)