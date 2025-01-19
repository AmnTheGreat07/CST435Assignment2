import pandas as pd
import numpy as np
import time

# Load matrices
A = pd.read_csv("matrix_A.csv", header=None).values
B = pd.read_csv("matrix_B.csv", header=None).values

# Start the timer
start_time = time.time()

# Calculate expected result
expected_C = np.dot(A, B)

# Stop the timer
end_time = time.time()

# Save the result to a CSV file
np.savetxt('single_thread_result_matrix.csv', expected_C, delimiter=',')

# Print the time taken
print(f"Time taken for single-threaded matrix multiplication: {end_time - start_time} seconds")

# Load the result from MPI program
C = pd.read_csv("result_matrix.csv", header=None).values

# Verify
assert np.allclose(C, expected_C), "Matrix multiplication result is incorrect!"
print("Matrix multiplication result is correct!")
