# CST435Assignment2

## Project Structure
```markdown
CST435Assignment2/
├── .gitignore                    # Git ignore file specifying files and directories to be ignored by version control
├── matrix_A.csv                  # CSV file storing matrix A
├── matrix_B.csv                  # CSV file storing matrix B
├── matrixs.py                    # Script to generate random matrices A and B and save them as CSV files
├── mpi_matrix_multiplication.py  # Implementation of matrix multiplication using MPI for parallel computation
├── multiplication.py             # Script containing functions for manual matrix multiplication
├── README.md                     # Project description file
├── result_matrix.csv             # CSV file storing the result of MPI parallel computation
├── single_thread_result_matrix.csv # CSV file storing the result of single-threaded computation
├── test.py                       # Test script to verify the correctness of MPI parallel computation results
```

## How to Run (For MPI)
1. Run the following command to generate random matrices A and B and save them as CSV files:
```bash
python matrixs.py
```
2. Run the following command to perform matrix multiplication using MPI for parallel computation:
```bash
mpiexec -n <number_of_processes> python mpi_matrix_multiplication.py
```
3. Run the following command to verify the correctness of the MPI parallel computation results:
```bash
python test.py
```
## Notice
- We must use this manual iterative algorithm to ensure consistency of comparison variables.
- The matrix multiplication algorithm is implemented in the `multiplication.py` file.