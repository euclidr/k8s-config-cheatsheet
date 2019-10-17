# create a service account have previleges to manage resource in a namespace
# there are predefined cluster roles that can be assign to a service account
# The most useful three cluster roles is:
# * system:aggregate-to-admin
# * system:aggregate-to-edit
# * system:aggregate-to-view
kubectl apply -f create_service_account.yaml # see file create_service_account.yaml

# You can list all cluster roles with command:
kubectl get clusterroles --all-namespaces
# than describe specific cluster role see its previleges
kubectl describe clusterroles <cluster_role_name>

# list service accounts in namespace
kubectl get sa -n <namespace>
# get secret name of a service account
kubectl get secret | grep <service_account_name> 
# describe secret, token the command shows can be used to login to kubernetes cluster
kubectl describe secret <secret_name>
