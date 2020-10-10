import csv
from datetime import datetime
import os


def get_results_path(results_folder_path):
    results_folder_path += datetime.now().strftime('%Y-%m-%d %H.%M.%S')

    if not os.path.isdir(results_folder_path):
        os.mkdir(results_folder_path)

    return results_folder_path


def write_results_to_file(file_path, results: dict):
    with open(file_path, mode='a+', newline='') as file:
        writer = csv.writer(file)

        # If the file is empty, add the column names.
        if os.stat(file_path).st_size == 0:
            writer.writerow(results.keys())

        writer.writerow(results.values())
