from kubernetes import client

from ..k8s_client.deployment import Deployment
from ..k8s_client.secret import Secret
from ..k8s_client.cluster_ip import ClusterIP
from ..k8s_client.ingress import Ingress
from .vars import *
from .constants import *


def create_image_secret(core_v1: client.CoreV1Api, secret_class_arguments_dict: dict):
    secret_object = Secret(
        api=core_v1, name=secret_class_arguments_dict["name"], username=secret_class_arguments_dict["username"],
        password=secret_class_arguments_dict["password"], server=secret_class_arguments_dict["server"], namespace=secret_class_arguments_dict["namespace"])
    is_created = secret_object.create_docker_registry_secret()
    return is_created


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


def delete_deployment_and_service(apps_v1: client.AppsV1Api, core_v1: client.CoreV1Api(), model_id: str):
    deployment_name = model_id + "-deployment"
    cluster_ip_name = model_id + "-cluster-ip"
    Deployment.delete_deployment(apps_v1, deployment_name, CLUSTER_NAMESPACE)
    ClusterIP.delete_cluster_ip(
        core_v1, cluster_ip_name, CLUSTER_NAMESPACE)


def create_ingress(networking_v1_api: client.NetworkingV1Api()):
    ingress_object = Ingress(networking_v1_api, name=INGRESS_NAME,
                             namespace=CLUSTER_NAMESPACE, ingress_class=INGRESS_CLASS)
    ingress_object.create_ingress()
    return ingress_object


def add_to_ingress(networking_v1_api: client.NetworkingV1Api(), model_id: str, service_info: dict):
    model_path = "/" + model_id + "/?(.*)"
    created_path_object = Ingress.create_ingress_path(
        model_path, service_info["service_name"], service_info["service_port"])
    Ingress.paths_list.append(created_path_object)
    Ingress.update_ingress_rules(
        networking_v1_api, INGRESS_NAME, CLUSTER_NAMESPACE)


def remove_from_ingress(networking_v1_api: client.NetworkingV1Api(), model_id: str, service_info: dict):
    model_path = "/" + model_id + "/?(.*)"
    created_path_object = Ingress.create_ingress_path(
        model_path,  service_info["service_name"], service_info["service_port"])
    if (created_path_object in Ingress.paths_list):
        Ingress.paths_list.remove(created_path_object)
        Ingress.update_ingress_rules(
            networking_v1_api, INGRESS_NAME, CLUSTER_NAMESPACE)
