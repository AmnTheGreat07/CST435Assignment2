import pandas as pd
import numpy as np

# Load matrices
A = pd.read_csv("matrix_A.csv", header=None).values
B = pd.read_csv("matrix_B.csv", header=None).values
C = pd.read_csv("result_matrix.csv", header=None).values

# Calculate expected result
expected_C = np.dot(A, B)

# Verify
assert np.allclose(C, expected_C), "Matrix multiplication result is incorrect!"
print("Matrix multiplication result is correct!")
