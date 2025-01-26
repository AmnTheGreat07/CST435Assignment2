#!/usr/bin/env python3
import sys
from collections import defaultdict

# Dictionary to aggregate partial results
result = defaultdict(float)

def process_line(line):
    key, value = line.strip().split("\t")
    row_idx, col_idx = map(int, key.split(","))
    result[(row_idx, col_idx)] += float(value)

if __name__ == "__main__":
    for line in sys.stdin:
        process_line(line)

    # Output final results in sorted order
    for (row_idx, col_idx), value in sorted(result.items()):
        print(f"{row_idx},{col_idx}\t{value}")