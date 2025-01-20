## Tree Structure
```
MPI/
├── Dockerfile
├── matrix_A.csv
├── matrix_B.csv
├── matrixs.py
├── mpi_matrix_multiplication.py
├── multiplication.py
├── README.md
├── requirements.txt
├── result_matrix.csv
├── single_thread_result_matrix.csv
└── test.py
```
## Files Description
- `Dockerfile`: Dockerfile for building the docker image.
- `matrix_A.csv`: Random matrix A.
- `matrix_B.csv`: Random matrix B.
- `matrixs.py`: Python script to generate random matrices A and B and save them as CSV files.
- `mpi_matrix_multiplication.py`: Python script to run the MPI parallel computation.
- `multiplication.py`: Python script to implement the matrix multiplication algorithm.
- `README.md`: Instructions on how to run the MPI matrix multiplication.
- `requirements.txt`: Required packages for the docker image.
- `result_matrix.csv`: Result matrix after the MPI parallel computation.
- `single_thread_result_matrix.csv`: Result matrix after the single-thread computation.
- `test.py`: Python script to test the matrix multiplication algorithm.

## How to Run (For MPI)
1. Run the following command to generate random matrices A and B and save them as CSV files:
```bash
python matrixs.py
```
2. Build the docker image:
```bash
docker build -t mpi_ssh_image .
```
3. Create a docker network:
```bash
docker network create mpi_network
```
4. Run the docker container (based on your nodes count):
```bash
docker run -d --network mpi_network --name mpi_container1 mpi_ssh_image
docker run -d --network mpi_network --name mpi_container2 mpi_ssh_image
...
```
5. Get the IP address or hostname of the containers for update the `hosts` file:
```bash
docker inspect mpi_container1 | grep IPAddress
docker inspect mpi_container2 | grep IPAddress
```
6. To the main container:
```bash
docker exec -it mpi_container1 bash
```
7. Update/create the `hosts` file:
```bash
echo "ipaddress1" > hosts
echo "ipaddress2" >> hosts
...
```
8.In main container, Run the following command to run the MPI parallel computation (n=number of nodes):
```bash
mpiexec -f hosts -n 2 python mpi_matrix_multiplication.py
```