from kubernetes import client, config

from .helpers import *
from .constants import *


def startup():
    apps_v1, core_v1, networking_v1_api = __initialize_k8s_client__()
    startup_config_dict = {
        "apps_v1": apps_v1,
        "core_v1": core_v1,
        "networking_v1_api": networking_v1_api,
        "ingress_object": None
    }
    if not __is_cluster_initialized__(apps_v1, networking_v1_api):
        try:
            startup_config_dict["ingress_object"] = __initialize_cluster_resources__(
                apps_v1, core_v1, networking_v1_api)
        except Exception as e:
            print("Cannot initialize cluster resources.")
            print(e)

    return startup_config_dict


def __initialize_k8s_client__():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()
    networking_v1_api = client.NetworkingV1Api()
    return apps_v1, core_v1, networking_v1_api


def __is_cluster_initialized__(apps_v1: client.AppsV1Api, networking_v1_api: client.NetworkingV1Api()):
    created_ingresses = Ingress.get_ingresses(
        networking_v1_api, CLUSTER_NAMESPACE)
    created_deployments = Deployment.get_deployments(
        apps_v1, CLUSTER_NAMESPACE)

    if (len(created_ingresses) == 0 or len(created_deployments) == 0):
        return False

    return True


def __initialize_cluster_resources__(apps_v1: client.AppsV1Api, core_v1: client.CoreV1Api(), networking_v1_api: client.NetworkingV1Api()):
    is_created = create_image_secret(core_v1, secret_class_arguments_dict)
    default_deployment_class_arguments["secret_name"] = IMAGE_SECRET_NAME
    default_deployment_object, default_cluster_ip_object = create_deployment_and_service(
        apps_v1, core_v1, default_deployment_class_arguments, default_cluster_ip_class_arguments_dict)

    ingress_object = create_ingress(networking_v1_api)
    return ingress_object
