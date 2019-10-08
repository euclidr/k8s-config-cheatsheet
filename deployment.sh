kubectl apply -f deployment.yaml

kubectl delete -f deployment.yaml

kubectl describe deployment <deployment-name>
kubectl describe deployment <deployment-name> -o yaml
kubectl get deployment <deployment-name> -o yaml # almost the same with the above

# if there're pods in deployment unavailable
# you can get their names and describe them to find the reasons.
kubectl get pods
kubectl describe pod <pod-name>