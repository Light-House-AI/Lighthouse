from .helpers import *
from .startup import *
from ..k8s_client.ingress import Ingress


def add_main_ingress_path():
    if len(Ingress.paths_list) == 0:
        main_path_object = Ingress.create_ingress_path(
            path="/?(.*)", service_name=DEFAULT_MODEL_ID+"-cluster-ip", service_port=DEFAULT_CLUSTER_IP_PORT)
        Ingress.paths_list.append(main_path_object)


def deploy_model(model_id: str, startup_config_dict: dict):
    deployment_envs_dict["AZURE_BLOB_NAME"] = model_id + PKL_EXTENTION
    deployment_class_arguments["model_id"] = cluster_ip_class_arguments_dict["model_id"] = model_id
    deployment_class_arguments["secret_name"] = IMAGE_SECRET_NAME
    try:
        deployment_object, cluster_ip_object = create_deployment_and_service(
            startup_config_dict["apps_v1"], startup_config_dict["core_v1"], deployment_class_arguments, cluster_ip_class_arguments_dict)
        service_info = {
            "service_name": deployment_class_arguments["model_id"]+"-cluster-ip",
            "service_port": cluster_ip_class_arguments_dict["port"],
        }
        add_to_ingress(
            startup_config_dict["networking_v1_api"], model_id, service_info)
    except Exception as e:
        print(
            f"Error in deploying model {model_id}")
        print(e)


def delete_model(model_id: str, startup_config_dict: dict):
    deployment_class_arguments["model_id"] = cluster_ip_class_arguments_dict["model_id"] = model_id
    try:
        delete_deployment_and_service(
            startup_config_dict["apps_v1"], startup_config_dict["core_v1"], model_id)
        service_info = {
            "service_name": deployment_class_arguments["model_id"]+"-cluster-ip",
            "service_port": cluster_ip_class_arguments_dict["port"],
        }
        remove_from_ingress(
            startup_config_dict["networking_v1_api"], model_id, service_info)
    except Exception as e:
        print(f"Error in deleting model {model_id}")
        print(e)


def recreate_ingress_rules(models_list: list, startup_config_dict: dict):
    for model_id in models_list:
        deployment_class_arguments["model_id"] = cluster_ip_class_arguments_dict["model_id"] = model_id
        service_info = {
            "service_name": deployment_class_arguments["model_id"]+"-cluster-ip",
            "service_port": cluster_ip_class_arguments_dict["port"],
        }
        add_to_ingress(
            startup_config_dict["networking_v1_api"], model_id, service_info)
