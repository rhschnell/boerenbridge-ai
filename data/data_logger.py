import csv
import os

class DataLogger:
    def __init__(self, path):
        self.path = path
        self.file_exists = os.path.exists(path)

    def log(self, row):
        with open(self.path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not self.file_exists:
                writer.writeheader()
                self.file_exists = True
            writer.writerow(row)