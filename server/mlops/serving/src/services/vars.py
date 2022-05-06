from services.constants import *

# TODO Read fom script
secret_class_arguments_dict = {
    "name": "secret-name",
    "username": "image repo user name",
    "password": "your password",
    "server": "your docker registry server",
    "namespace": CLUSTER_NAMESPACE
}
# TODO Read fom script
# TODO: Blob name = model_id + PKL_EXTENTION
deployment_envs_dict = {
    "AZURE_STORAGE_CONNECTION_STRING": "your connection string",
    "AZURE_CONTAINER_NAME": "models",
    "AZURE_BLOB_NAME": "classifier1" + PKL_EXTENTION,
}
# TODO Read fom script
deployment_class_arguments = {
    "model_id": "label",
    "namespace": CLUSTER_NAMESPACE,
    "replicas": 1,
    "image": IMAGE_NAME,
    "env_vars": deployment_envs_dict,
    "secret_name": "leave as is. DO NOT CHANGE"
}

cluster_ip_class_arguments_dict = {
    "model_id": deployment_class_arguments["model_id"],
    "namespace": CLUSTER_NAMESPACE,
    "port": DEFAULT_CLUSTER_IP_PORT,
    "target_port": DEFAULT_CLUSTER_IP_TARGET_PORT
}

default_deployment_class_arguments = {
    "model_id": DEFAULT_DEPLOYMENT_NAME,
    "namespace": CLUSTER_NAMESPACE,
    "replicas": 1,
    "image": DEFAULT_IMAGE_NAME,
    "env_vars": {},
    "secret_name": "leave as is. DO NOT CHANGE"
}
default_cluster_ip_class_arguments_dict = {
    "model_id": DEFAULT_DEPLOYMENT_NAME,
    "namespace": CLUSTER_NAMESPACE,
    "port": DEFAULT_CLUSTER_IP_PORT,
    "target_port": DEFAULT_CLUSTER_IP_TARGET_PORT

}
