# Kubernetes resources definition

This program aims at creating readable pages for Kubernetes resources.

You can a more detailed specification in page: https://kubernetes.io/docs/reference/kubernetes-api/

# How to get Kubernetes openapi difinition

1. Login to a machine with kubectl that can access to the cluster
2. Run `kubectl proxy`
3. When `kubectl proxy` is running, run bellow in another terminal
    ```
    curl localhost:8001/openapi/v2 -o swagger.json
    ```

# How to get api-resources.txt

1. Login to a machine with kubectl that can access to the cluster
2. Run `kubectl api-resources > api-resources.txt`