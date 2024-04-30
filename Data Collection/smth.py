import csv

input_file_name = 'param_sweep_clean.csv'
output_file_name = 'modified_example.csv'

with open(input_file_name, mode='r', newline='') as input_file, open(output_file_name, mode='w', newline='') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)
    
    headers = next(csv_reader)
    csv_writer.writerow(['Experiment Number'] + headers)
    
    for row_index, row in enumerate(csv_reader, start=1):
        csv_writer.writerow([row_index] + row)

print("CSV file has been modified and saved as 'modified_example.csv'.")
