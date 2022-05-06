from kubernetes import client, config

from services.helpers import *


def startup():
    apps_v1, core_v1, networking_v1_api = initialize_k8s_client()
    if not is_cluster_initialized(apps_v1, networking_v1_api):
        try:
            secret_name, ingress_object = initialize_cluster_resources(
                apps_v1, core_v1, networking_v1_api)
        except Exception as e:
            print("Cannot initialize cluster resources.")
            print(e)
    # TODO secret_name has to be saved somewhere
    return apps_v1, core_v1, networking_v1_api, secret_name, ingress_object


def initialize_k8s_client():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()
    networking_v1_api = client.NetworkingV1Api()
    return apps_v1, core_v1, networking_v1_api


def is_cluster_initialized(apps_v1: client.AppsV1Api, networking_v1_api: client.NetworkingV1Api()):
    created_ingresses = Ingress.get_ingresses(
        networking_v1_api, CLUSTER_NAMESPACE)
    created_deployments = Deployment.get_deployments(
        apps_v1, CLUSTER_NAMESPACE)

    if (len(created_ingresses) == 0 or len(created_deployments) == 0):
        return False

    return True


def initialize_cluster_resources(apps_v1: client.AppsV1Api, core_v1: client.CoreV1Api(), networking_v1_api: client.NetworkingV1Api(),):
    secret_name = create_image_secret(core_v1, secret_class_arguments_dict)

    default_deployment_class_arguments["secret_name"] = secret_name
    default_deployment_object, default_cluster_ip_object = create_deployment_and_service(
        apps_v1, core_v1, default_deployment_class_arguments, default_cluster_ip_class_arguments_dict)

    ingress_object = create_ingress(networking_v1_api)
    return secret_name, ingress_object
