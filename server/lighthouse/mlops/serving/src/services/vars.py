from services.constants import *

# TODO username & password
secret_class_arguments_dict = {
    "name": IMAGE_SECRET_NAME,
    "username": "username",
    "password": "password",
    "server": IMAGE_SERVER,
    "namespace": CLUSTER_NAMESPACE
}
# TODO azure_connection_string
deployment_envs_dict = {
    "AZURE_STORAGE_CONNECTION_STRING": "",
    "AZURE_CONTAINER_NAME": CONTAINER_NAME,
    "DEPLOYMENT_TYPE": "leave as is",
    "AZURE_BLOB_NAME": "leave as is" + PKL_EXTENSION,
    "AZURE_BLOB_NAME_2": "leave as is" + PKL_EXTENSION,
}
deployment_class_arguments = {
    "project_id": "leave as it",
    "namespace": CLUSTER_NAMESPACE,
    "replicas": 1,
    "image": IMAGE_NAME,
    "env_vars": deployment_envs_dict,
    "secret_name": "leave as is. DO NOT CHANGE"
}
cluster_ip_class_arguments_dict = {
    "project_id": deployment_class_arguments["project_id"],
    "namespace": CLUSTER_NAMESPACE,
    "port": DEFAULT_CLUSTER_IP_PORT,
    "target_port": DEFAULT_CLUSTER_IP_TARGET_PORT
}
default_deployment_class_arguments = {
    "project_id": DEFAULT_PROJECT_ID,
    "namespace": CLUSTER_NAMESPACE,
    "replicas": 1,
    "image": DEFAULT_IMAGE_NAME,
    "env_vars": {},
    "secret_name": "leave as is. DO NOT CHANGE"
}
default_cluster_ip_class_arguments_dict = {
    "project_id": DEFAULT_PROJECT_ID,
    "namespace": CLUSTER_NAMESPACE,
    "port": DEFAULT_CLUSTER_IP_PORT,
    "target_port": DEFAULT_CLUSTER_IP_TARGET_PORT
}
