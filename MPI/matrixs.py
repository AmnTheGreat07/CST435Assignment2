import numpy as np

# Generate random matrices
matrix_A = np.random.randint(low=0, high=100, size=(800, 500))
matrix_B = np.random.randint(low=0, high=100, size=(500, 800))

# Save matrices to CSV files with integer format
np.savetxt('matrix_A.csv', matrix_A, delimiter=',', fmt='%d')
np.savetxt('matrix_B.csv', matrix_B, delimiter=',', fmt='%d')