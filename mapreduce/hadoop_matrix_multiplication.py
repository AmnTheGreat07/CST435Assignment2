import os
import numpy as np
import subprocess
import argparse

def read_matrix(file_path):
    """Reads a matrix from a CSV file."""
    return np.loadtxt(file_path, delimiter=',')

def prepare_input(matrix_a_file, matrix_b_file, output_dir):
    """
    Converts matrix A into key-value pairs and writes it to the input directory.
    Matrix B is saved as-is to be distributed to all mappers.
    """
    matrix_a = read_matrix(matrix_a_file)
    matrix_b = read_matrix(matrix_b_file)

    if matrix_a.shape[1] != matrix_b.shape[0]:
        raise ValueError("Matrix A columns must match Matrix B rows.")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Save matrix B to the output directory
    np.savetxt(os.path.join(output_dir, "matrix_B.csv"), matrix_b, delimiter=',')

    # Write each row of matrix A as a key-value pair
    with open(os.path.join(output_dir, "matrix_A.txt"), 'w') as f:
        for i, row in enumerate(matrix_a):
            row_str = ','.join(map(str, row))
            f.write(f"{i}\t{row_str}\n")

    print(f"Input files prepared in {output_dir}")

def run_mapreduce(input_dir, output_dir, hadoop_streaming_path):
    """
    Runs the MapReduce job using the Hadoop streaming jar.
    """
    mapper_script = os.path.abspath("mapper.py")
    reducer_script = os.path.abspath("reducer.py")
    matrix_b_path = os.path.join(input_dir, "matrix_B.csv")

    # Ensure the output directory is clean
    subprocess.run(["hadoop", "fs", "-rm", "-r", output_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Upload input files to HDFS
    subprocess.run(["hadoop", "fs", "-mkdir", "-p", "/input"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["hadoop", "fs", "-put", f"{input_dir}/matrix_A.txt", "/input"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["hadoop", "fs", "-put", f"{matrix_b_path}", "/input"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Run the Hadoop MapReduce job
    subprocess.run([
        "hadoop", "jar", hadoop_streaming_path,
        "-input", "/input/matrix_A.txt",
        "-output", output_dir,
        "-mapper", f"python3 {mapper_script}",
        "-reducer", f"python3 {reducer_script}",
        "-file", mapper_script,
        "-file", reducer_script,
        "-file", matrix_b_path
    ])

    print(f"MapReduce job completed. Results saved to {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Matrix Multiplication with Hadoop MapReduce")
    parser.add_argument("--prepare_input", action="store_true", help="Prepare input files for MapReduce.")
    parser.add_argument("--run_job", action="store_true", help="Run the MapReduce job.")
    parser.add_argument("--matrix_a", type=str, default="matrix_A.csv", help="Path to matrix A CSV file.")
    parser.add_argument("--matrix_b", type=str, default="matrix_B.csv", help="Path to matrix B CSV file.")
    parser.add_argument("--output_dir", type=str, default="mapreduce_input", help="Directory to store input/output files.")
    parser.add_argument("--hadoop_streaming_path", type=str, required=False, help="Path to Hadoop streaming jar.")
    args = parser.parse_args()

    if args.prepare_input:
        prepare_input(args.matrix_a, args.matrix_b, args.output_dir)

    if args.run_job:
        if not args.hadoop_streaming_path:
            raise ValueError("You must specify the Hadoop streaming jar path using --hadoop_streaming_path.")
        run_mapreduce(args.output_dir, "/output", args.hadoop_streaming_path)

if __name__ == "__main__":
    main()
