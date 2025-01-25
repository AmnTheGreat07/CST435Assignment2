## Tree Structure
```
MPI/
├── deployment.yaml
├── Dockerfile
├── matrix_A.csv
├── matrix_B.csv
├── matrixs.py
├── mpi_matrix_multiplication.py
├── multiplication.py
├── README.md
├── requirements.txt
├── service.yaml
├── result_matrix.csv
├── single_thread_result_matrix.csv
└── test.py
```
## Files Description
- `deployment.yaml`: Kubernetes deployment file for the MPI matrix multiplication.
- `Dockerfile`: Dockerfile for building the docker image.
- `matrix_A.csv`: Random matrix A.
- `matrix_B.csv`: Random matrix B.
- `matrixs.py`: Python script to generate random matrices A and B and save them as CSV files.
- `mpi_matrix_multiplication.py`: Python script to run the MPI parallel computation.
- `multiplication.py`: Python script to implement the matrix multiplication algorithm.
- `README.md`: Instructions on how to run the MPI matrix multiplication.
- `requirements.txt`: Required packages for the docker image.
- `service.yaml`: Kubernetes service file for the MPI matrix multiplication.
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
8. In main container, Run the following command to run the MPI parallel computation (n=number of nodes):
```bash
mpiexec -f hosts -n 2 python mpi_matrix_multiplication.py
```

## How to Run In K8s (Minikube)
1. Install minikube  
[Minikube Installation](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download#Service)  
Minikube is a tool that makes it easy to run Kubernetes locally. Minikube runs a  Kubernetes cluster inside a VM on your laptop for users looking to try out Kubernetes or develop with it day-to-day.  

- For Linux:
```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```
2. Start minikube (2 CPUs, 4GB RAM / per node)(2nodes):
```bash
minikube start --nodes 2 --cpus 2 --memory 4096
```
3. Generate SSH key (in the same directory):
```bash
ssh-keygen -t rsa -f id_rsa -q -N ""
```
- After that, you will have 2 files: `id_rsa` and `id_rsa.pub`.  
4. Create a Kubernetes secret:
```bash
kubectl create secret generic ssh-keys \
  --from-file=id_rsa=./id_rsa \
  --from-file=id_rsa.pub=./id_rsa.pub \
  --from-file=authorized_keys=./id_rsa.pub
```
5. Import the docker image to minikube  
(Assuming you have the docker image mpi_ssh_image:latest):
```bash
minikube image load mpi_ssh_image:latest
```
6. Apply the k8s yaml file:
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```
7. See the pods:
```bash
kubectl get pods -o wide
```
- You will see the IP addresses of the nodes.
```bash
NAME                              READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
mpi-deployment-7b655bd86f-56h7n   1/1     Running   0          54m   10.244.1.2   minikube-m02   <none>           <none>
mpi-deployment-7b655bd86f-wxqkg   1/1     Running   0          54m   10.244.0.3   minikube       <none>           <none>
```
8. To the main container  
(mpi-deployment-7b655bd86f-wxqkg is my pot name, you can see your pod name with `kubectl get nodes -o wide`):
```bash
kubectl exec -it mpi-deployment-7b655bd86f-wxqkg -- /bin/bash
```
9. Update/create the `hosts` file:
```bash
echo "your node1 ip" > hosts
echo "your node2 ip" >> hosts
...
```
10. Run the following command to run the MPI parallel computation (n=number of nodes):
```bash
mpiexec -f hosts -n 2 python mpi_matrix_multiplication.py
```
11. To see the result (run in node bash):
```bash
python test.py
```
## How to Run In K8s (Microk8s)
1. Install microk8s in every node   
Microk8s is a lightweight Kubernetes distribution that runs entirely on your workstation or edge device. It is a great solution for users who want to get a Kubernetes cluster up and running quickly.   
- For Ubuntu:
```bash
sudo snap install microk8s --classic
```
2. Initialize microk8s master node
```bash
microk8s enable dns hostpath-storage
```
3. Get the add token from the master node
```bash
microk8s add-node
```
- you will get a command like this:
```bash
microk8s join 10.0.2.15:25000/271e352934d8bd01cd115a3149e0ff23/be48c19219bf

Use the '--worker' flag to join a node as a worker not running the control plane                                     , eg:
microk8s join 10.0.2.15:25000/271e352934d8bd01cd115a3149e0ff23/be48c19219bf --wo                                     rker

If the node you are adding is not reachable through the default interface you ca                                     n use one of the following:
microk8s join 10.0.2.15:25000/271e352934d8bd01cd115a3149e0ff23/be48c19219bf
microk8s join 192.168.1.11:25000/271e352934d8bd01cd115a3149e0ff23/be48c19219bf
microk8s join 172.17.0.1:25000/271e352934d8bd01cd115a3149e0ff23/be48c19219bf
```
4. Add the worker node to the master node
```bash
microk8s join ip:port/token
```
- You will see the following message:
```bash
Successfully joined the cluster.
```
- You also can check the nodes with the following command:
```bash
microk8s kubectl get nodes
```
```bash
NAME          STATUS   ROLES    AGE   VERSION
kogasanet01   Ready    <none>   15s   v1.31.4
kogasanet02   Ready    <none>   99m   v1.31.4
```
5. Create a Docker image   
Follow the same steps as in the [Minikube seection](#how-to-run-in-k8s-minikube).   
Save Docker image to tar file.
```bash
docker save mpi_ssh_image:latest > mpi.tar
```
6. Import the docker image to every node
```bash
microk8s ctr image import mpi.tar
```
7. Create a Kubernetes secret   
Follow the same steps as in the [Minikube seection](#how-to-run-in-k8s-minikube).
(using kubectl in microk8s to instead kubeclt)
```bash
microk8s kubectl create secret generic ssh-keys \
  --from-file=id_rsa=./id_rsa \
  --from-file=id_rsa.pub=./id_rsa.pub \
  --from-file=authorized_keys=./id_rsa.pub
```
8. Apply the k8s yaml file
```bash
microk8s kubectl apply -f deployment.yaml
microk8s kubectl apply -f service.yaml
```
9. See the pods
```bash
microk8s kubectl get pods -o wide
```
```bash
NAME                             READY   STATUS    RESTARTS   AGE     IP             NODE          NOMINATED NODE   READINESS GATES
mpi-deployment-5c6d55765-gktct   1/1     Running   0          9m48s   10.1.147.202   kogasanet02   <none>           <none>
mpi-deployment-5c6d55765-xhpkv   1/1     Running   0          9m48s   10.1.212.1     kogasanet01   <none>           <none>
```
10. To the main container
```bash
microk8s kubectl exec -it "Your pods name" -- /bin/bash
```
11. Set hosts & Run MPI & Test   
Follow the same steps (9,10,11) as in the [Minikube seection](#how-to-run-in-k8s-minikube).

---
Note test.py is signal thread multiplication. You can see the difference between the signal thread and MPI.  

For example:
```python
matrix_A = np.random.randint(low=0, high=100, size=(800, 500))
matrix_B = np.random.randint(low=0, high=100, size=(500, 800))
```
Using MPI in k8s (2 nodes):
```bash
root@mpi-deployment-7b655bd86f-wxqkg:/app# mpiexec -f hosts -n 2 python mpi_matrix_multiplication.py
Rank 1 is processing rows 400
Rank 0 is processing rows 400
Time taken for manual matrix multiplication: 75.96773755899994 seconds
```
Test.py (signal thread):
```bash
root@mpi-deployment-7b655bd86f-wxqkg:/app# python test.py 
Time taken for single-threaded manual matrix multiplication: 163.4807047843933 seconds
Matrix multiplication result is correct!
```


