import os
import glob
import pandas as pd
import ydata_profiling as pp

# Path to the folder with CSV files
folder_path = './D2/data/stooq_data_2023-05-05'

# Path to the folder for EDA reports
output_folder_path = './D2/data/stooq_data_2023-05-05/automatic_eda'

# Create the output folder if it doesn't exist
try:
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
except OSError as error:
    print(f"Error creating output folder: {error}")
    exit(1)

# Get a list of CSV files in the folder
try:
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
except OSError as error:
    print(f"Error getting list of CSV files: {error}")
    exit(1)

# Iterate over each CSV file and generate a report
for file in csv_files:
    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(file)
    except OSError as error:
        print(f"Error reading file '{file}': {error}")
        continue

    # Generate a report with pandas profiling
    report = pp.ProfileReport(df, title=os.path.splitext(os.path.basename(file))[0])

    # Save the report to an HTML file in the output folder
    output_file_path = os.path.join(output_folder_path, os.path.splitext(os.path.basename(file))[0] + '_report.html')
    try:
        report.to_file(output_file_path)
    except OSError as error:
        print(f"Error saving report to file '{output_file_path}': {error}")
        continue
