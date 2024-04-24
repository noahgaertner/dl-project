import csv

# File names
input_file_name = 'param_sweep_clean.csv'
output_file_name = 'modified_example.csv'

# Open the input file in read mode and output file in write mode
with open(input_file_name, mode='r', newline='') as input_file, open(output_file_name, mode='w', newline='') as output_file:
    # Create CSV reader and writer
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)
    
    # Optional: If your file includes headers and you want to keep them,
    # read and write the header row, potentially adjusting the first cell.
    headers = next(csv_reader)
    csv_writer.writerow(['Experiment Number'] + headers)
    
    # Read the input CSV file and write to the output CSV file with the row number minus one
    for row_index, row in enumerate(csv_reader, start=1):
        csv_writer.writerow([row_index] + row)

print("CSV file has been modified and saved as 'modified_example.csv'.")
