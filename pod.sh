# Enter interative shell of the first container of a pod
kubectl exec -it <pod-name> -- /bin/sh
# Run a command in the first container of a pod
kubectl exec <pod-name> ls
# Run a command in a specific container of a pod
kubectl exec <pod-name> ls -c <container-name>
# Run complicate command
kubectl exec <pod-name> -- ls -alh /data

# Copy files from or to a container
kubectl cp <pod-name>:<file-or-folder-path> <destination-path-with-the-file-folder-name> -c <container-name>
kubectl cp <file-or-folder-path> <pod-name>:<destination-path-with-the-file-folder-name>

# Attach to the first container of a pod
kubectl attach <pod-name>
# Attach to the specific container of a pod
kubectl attach <pod-name> -c <container-name>
# If the container runs bash, you can attach to it interactively
kubectl attach <pod-name> -c <container-name> -i -t
# Attach to the first pod in an app
kubectl attach deploy/<deploment-name>
kubectl attach rs/<replicaset-name>

# Show logs of pods in statefulset, also work for deployments, replicasets
kubectl logs sts/<statefulsets-name> --all-containers --tail 10
# Show logs of the first container of a pod
kubectl logs <pod-name>

# Forward port 80 of a pod in deploy/nginx-deploy-try to local port 5000
# The pod is chosen by deployment
kubectl port-forward deploy/nginx-deploy-try 5000:80
# Specify local addresses to bind to
kubectl port-forward deploy/nginx-deploy-try 5000:80 --address localhost,10.19.21.23
# Forward port 80 of a pod to local port 5000
kubectl port-forward <pod-name> 5000:80
# Forward two port to local, port numbers of both sides are the same
kubectl port-forward <pod-name> 5000 6000

