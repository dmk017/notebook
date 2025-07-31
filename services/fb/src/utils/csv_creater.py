import csv
import os

def create_sample_csv(file_path: str, encoding: str, header: list[str], data: list[str] = [], delimeter: str = ','):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w+', encoding=encoding) as f:
        wr = csv.writer(f, delimiter=delimeter)
        wr.writerow(header)
        wr.writerow(data)
    return file_path
