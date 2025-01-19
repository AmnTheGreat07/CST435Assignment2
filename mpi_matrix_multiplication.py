from mpi4py import MPI
import numpy as np
import pandas as pd

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define file paths for the matrices
matrix_a_file = "matrix_A.csv"
matrix_b_file = "matrix_B.csv"

# Initialize matrices
A = None
B = None

if rank == 0:
    # Master process reads matrices from CSV files
    A = pd.read_csv(matrix_a_file, header=None).values
    B = pd.read_csv(matrix_b_file, header=None).values

    # Validate dimensions
    if A.shape[1] != B.shape[0]:
        raise ValueError("Matrix dimensions do not match for multiplication!")

# Broadcast dimensions to all processes
A_rows, A_cols = None, None
B_rows, B_cols = None, None
if rank == 0:
    A_rows, A_cols = A.shape
    B_rows, B_cols = B.shape

A_rows = comm.bcast(A_rows, root=0)
A_cols = comm.bcast(A_cols, root=0)
B_rows = comm.bcast(B_rows, root=0)
B_cols = comm.bcast(B_cols, root=0)

# Scatter rows of matrix A among processes
local_A = np.zeros((A_rows // size, A_cols)) if rank != 0 else None
comm.Scatter(A, local_A, root=0)

# Broadcast entire matrix B to all processes
if rank != 0:
    B = np.zeros((B_rows, B_cols))
comm.Bcast(B, root=0)

# Compute local portion of the result matrix
local_C = np.dot(local_A, B)

# Gather results at the root process
C = None
if rank == 0:
    C = np.zeros((A_rows, B_cols))
comm.Gather(local_C, C, root=0)

# Root process writes the result matrix to a CSV file
if rank == 0:
    output_file = "result_matrix.csv"
    pd.DataFrame(C).to_csv(output_file, header=False, index=False)
    print(f"Matrix multiplication result saved to {output_file}")
