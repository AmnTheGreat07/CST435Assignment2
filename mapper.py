#!/usr/bin/env python3
import sys
import numpy as np

# Load matrix B once per mapper
matrix_b = np.loadtxt("matrix_B.csv", delimiter=",")

def process_line(line):
    row_idx, row_data = line.strip().split("\t")
    row_idx = int(row_idx)
    row = np.array([float(x) for x in row_data.split(",")])

    # Generate intermediate key-value pairs
    for col_idx in range(matrix_b.shape[1]):
        partial_sum = sum(row[i] * matrix_b[i, col_idx] for i in range(len(row)))
        print(f"{row_idx},{col_idx}\t{partial_sum}")

if __name__ == "__main__":
    for line in sys.stdin:
        process_line(line)