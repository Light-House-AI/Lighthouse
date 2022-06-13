from .constants import *
from lighthouse.config import config

secret_class_arguments_dict = {
    "name": IMAGE_SECRET_NAME,
    "username": config.GHCR_USERNAME,
    "password": config.GHCR_PASSWORD,
    "server": IMAGE_SERVER,
    "namespace": CLUSTER_NAMESPACE
}

deployment_envs_dict = {
    "AZURE_STORAGE_CONNECTION_STRING": config.AZURE_CONN_STR,
    "AZURE_CONTAINER_NAME": CONTAINER_NAME,
    "AZURE_BLOB_NAME": "leave as is" + PKL_EXTENTION,
}
deployment_class_arguments = {
    "model_id": "=leave as it",
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
    "model_id": DEFAULT_MODEL_ID,
    "namespace": CLUSTER_NAMESPACE,
    "replicas": 1,
    "image": DEFAULT_IMAGE_NAME,
    "env_vars": {},
    "secret_name": "leave as is. DO NOT CHANGE"
}
default_cluster_ip_class_arguments_dict = {
    "model_id": DEFAULT_MODEL_ID,
    "namespace": CLUSTER_NAMESPACE,
    "port": DEFAULT_CLUSTER_IP_PORT,
    "target_port": DEFAULT_CLUSTER_IP_TARGET_PORT
}
