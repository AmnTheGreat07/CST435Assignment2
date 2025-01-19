from mpi4py import MPI
import numpy as np
import time

def read_matrix(file_path):
    return np.loadtxt(file_path, delimiter=',')

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # Read matrices from CSV files
        matrix_A = read_matrix('matrix_A.csv')
        matrix_B = read_matrix('matrix_B.csv')

        # Check if matrices can be multiplied
        if matrix_A.shape[1] != matrix_B.shape[0]:
            raise ValueError("Number of columns in matrix A must be equal to number of rows in matrix B")

        # Split matrix A into chunks to distribute to other processes
        rows_A = np.array_split(matrix_A, size, axis=0)
    else:
        matrix_B = None
        rows_A = None

    # Scatter rows of matrix A to all processes
    rows_A = comm.scatter(rows_A, root=0)

    # Broadcast matrix B to all processes
    matrix_B = comm.bcast(matrix_B, root=0)

    # Start the timer
    comm.Barrier()  # Synchronize before starting the timer
    start_time = MPI.Wtime()

    # Perform local matrix multiplication
    local_result = np.dot(rows_A, matrix_B)

    # Gather results from all processes
    result = comm.gather(local_result, root=0)

    # Stop the timer
    comm.Barrier()  # Synchronize before stopping the timer
    end_time = MPI.Wtime()

    if rank == 0:
        # Concatenate the results to form the final result matrix
        result = np.vstack(result)
        print("Resultant Matrix:")
        print(result)
        
        # Save the result to a CSV file
        np.savetxt('result_matrix.csv', result, delimiter=',')
        
        # Print the time taken
        print(f"Time taken for matrix multiplication: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()