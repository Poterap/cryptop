import os
import glob
import sys
import pandas as pd
import ydata_profiling as pp

import src.utils.file_functions as uti

class autoeda:

    def make_raport_from_directory(self, folder_path: str):
        """
        Funcion creates auto eda raports for csv files in given file directory. Raports are saved in html format. 
        """

        output_folder_path = uti.create_folder_in_directory(name='automatic_eda', path_directory=folder_path, add_date=False)

        # Get a list of CSV files in the folder
        try:
            csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
        except OSError as error:
            print(f"Error getting list of CSV files: {error}")
            exit(1)

        print(csv_files)

        # Iterate over each CSV file and generate a report
        for file in csv_files:
            print(file)
            # Load the CSV file into a DataFrame
            try:
                df = pd.read_csv(file)
            except Exception as error:
                print(f"Error reading file '{file}': {error}")
                continue

            if df.empty:
                print(f"Warning: Empty CSV file '{file}'. Skipping.")
                continue

            self.generate_auto_eda_raport(df, output_folder_path, file)


    def generate_auto_eda_raport(self, df, output_folder_path, file):
        """
        Funcion generate auto eda raport, and saves it in given folder 
        """

        # Gets symbol name from file
        symbol = os.path.splitext(os.path.basename(file))[0]

        # Generate a report with pandas profiling
        report = pp.ProfileReport(df, title=symbol)

        # Save the report to an HTML file in the output folder
        output_file_path = os.path.join(output_folder_path, symbol + '_report.html')

        try:
            report.to_file(output_file_path)

            print(output_file_path)
        except OSError as error:
            print(f"Error saving report to file '{output_file_path}': {error}")
                
