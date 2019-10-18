# reference: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap

# 6 ways to create configmap

# 1. create from config folder
# Folder files:
#   the_folder/
#     ui.properties
#     logic.properties
# Result in:
#   data:
#     ui.properties: /
#       screen_width: 40
#       screen_height: 60
#     ...
kubectl create configmap <name> --from-file=/path/to/the_folder/

# 2. create from config files
kubectl create configmap <name> --from-file=/path/to/the_folder/ui.properties --from-file=/path/to/the_folder/ui.properties
# you can also use custom key name instead of file name
kubectl create configmap <name> --from-file=ui=/path/to/the_folder/ui.properties

# 3. load config kv from file
kubectl create configmap <name> --from-env-file=/path/to/the_folder/ui.properties
kubectl create configmap <name> --from-env-file=/path/to/the_folder/ui2.properties # all previous data will be replaced
kubectl create configmap <name> --from-env-file=/path/to/the_folder/ui.properties --from-env-file=/path/to/the_folder/logic.properties

# 4. create from literals
kubectl create configmap <name> --from-literal=key1=value1 --from-literal=key2=value2

# 5. sometimes you want to create a configmap from a template with a name prefix
# ref: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#create-a-configmap-from-generator
# Create a kustomization.yaml file with ConfigMapGenerator
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: game-config-4
  files:
  - configure-pod-container/configmap/game.properties
EOF
kubectl apply -k .
configmap/game-config-4-m9dm2f92bt created

# 6. create from resource definition
kubctl -apply -f <configmap_file.yaml>


# ------
# configmap can be used with ENV or mounted file
# take `dapi-test-pod1` and `dapi-test-pod2` in  configmap-template.yaml as an example
