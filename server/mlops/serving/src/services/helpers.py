from kubernetes import client

from k8s_client.deployment import Deployment
from k8s_client.secret import Secret
from k8s_client.cluster_ip import ClusterIP
from k8s_client.ingress import Ingress
from services.vars import *
from services.constants import *


def create_image_secret(core_v1: client.CoreV1Api, secret_class_arguments_dict: dict):
    secret_object = Secret(
        api=core_v1, name=secret_class_arguments_dict["name"], username=secret_class_arguments_dict["username"],
        password=secret_class_arguments_dict["password"], server=secret_class_arguments_dict["server"], namespace=secret_class_arguments_dict["namespace"])
    secret_name = secret_object.create_docker_registry_secret()
    return secret_name


def create_deployment_and_service(apps_v1: client.AppsV1Api, core_v1: client.CoreV1Api(), deployment_class_arguments: dict,
                                  cluster_ip_class_arguments_dict: dict):
    deployment_object = create_deployment(apps_v1, deployment_class_arguments)
    cluster_ip_object = create_cluster_ip(
        core_v1, cluster_ip_class_arguments_dict)

    return deployment_object, cluster_ip_object


def create_deployment(apps_v1: client.AppsV1Api, deployment_class_arguments: dict):
    deployment_object = Deployment(api=apps_v1, model_id=deployment_class_arguments["model_id"], namespace=deployment_class_arguments["namespace"],
                                   replicas=deployment_class_arguments[
                                       "replicas"], image=deployment_class_arguments["image"],
                                   env_vars=deployment_class_arguments["env_vars"], secret_name=deployment_class_arguments["secret_name"])
    deployment_object.create_deployment()
    return deployment_object


def create_cluster_ip(core_v1: client.CoreV1Api, cluster_ip_class_arguments_dict: dict):
    cluster_ip_object = ClusterIP(
        api=core_v1, model_id=cluster_ip_class_arguments_dict[
            "model_id"], namespace=cluster_ip_class_arguments_dict["namespace"], port=cluster_ip_class_arguments_dict["port"],
        target_port=cluster_ip_class_arguments_dict["target_port"])
    cluster_ip_object.create_cluster_ip()
    return cluster_ip_object


def create_ingress(networking_v1_api: client.NetworkingV1Api()):
    ingress_object = Ingress(networking_v1_api, name=INGRESS_NAME,
                             namespace=CLUSTER_NAMESPACE, ingress_class=INGRESS_CLASS, default_service_name=DEFAULT_DEPLOYMENT_NAME,
                             default_port_number=DEFAULT_CLUSTER_IP_PORT)
    ingress_object.create_ingress()
    return ingress_object
