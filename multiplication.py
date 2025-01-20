import numpy as np

def manual_matrix_multiply(A, B):
    """
    Perform matrix multiplication manually using nested loops.

    Parameters:
    A (numpy.ndarray): Matrix A of size (m, n)
    B (numpy.ndarray): Matrix B of size (n, p)

    Returns:
    numpy.ndarray: Resultant matrix of size (m, p)
    """
    # Initialize the result matrix with zeros
    result = np.zeros((A.shape[0], B.shape[1]))

    # Perform manual matrix multiplication
    for i in range(A.shape[0]):  # Iterate over rows of A
        for j in range(B.shape[1]):  # Iterate over columns of B
            for k in range(A.shape[1]):  # Iterate over columns of A / rows of B
                result[i, j] += A[i, k] * B[k, j]
    return result
