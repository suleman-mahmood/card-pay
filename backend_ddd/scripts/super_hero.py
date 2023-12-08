### ### ### ### ### ###
### Setup variables
### ### ### ### ### ###

"""
Steps when integrating a new API
1. Create a cubit file
2. Create a state file
3. Add a new API to python API service
4. Add a new function to abstract API Repository
5. Implement this function in Fake Repository
6. Implement this function in Repository Imp
7. Create Response model
8. Create Request model
9. Run python generator
"""

"""
Snippets:
- BlocBuilder
- BlocConsumer
- BlocListener
"""


def copy_file(input_file_path, output_file_path):
    try:
        # Open the input file for reading
        with open(input_file_path, "r") as input_file:
            # Open the output file for writing
            with open(output_file_path, "w") as output_file:
                # Read each line from the input file and write it to the output file
                for line in input_file:
                    output_file.write(line)
        print("File copied successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
input_file_path = "input.txt"  # Replace with the path to your input file
output_file_path = "output.txt"  # Replace with the desired path for the output file

copy_file(input_file_path, output_file_path)
