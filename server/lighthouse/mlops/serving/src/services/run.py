from services.helpers import *
from services.startup import *
from k8s_client.ingress import Ingress


def add_main_ingress_path():
    if len(Ingress.paths_list) == 0:
        main_path_object = Ingress.create_ingress_path(
            path="/?(.*)", service_name=DEFAULT_PROJECT_ID+"-cluster-ip", service_port=DEFAULT_CLUSTER_IP_PORT)
        Ingress.paths_list.append(main_path_object)


def deploy_model(startup_config_dict: dict, project_id: str, deployment_type: str, model_id: str, challenger_model_id: str = "None"):
    deployment_envs_dict["DEPLOYMENT_TYPE"] = deployment_type
    deployment_envs_dict["AZURE_BLOB_NAME"] = model_id + PKL_EXTENSION
    deployment_envs_dict["AZURE_BLOB_NAME_2"] = challenger_model_id + PKL_EXTENSION
    deployment_class_arguments["project_id"] = cluster_ip_class_arguments_dict["project_id"] = project_id
    deployment_class_arguments["secret_name"] = IMAGE_SECRET_NAME
    try:
        deployment_object, cluster_ip_object = create_deployment_and_service(
            startup_config_dict["apps_v1"], startup_config_dict["core_v1"], deployment_class_arguments, cluster_ip_class_arguments_dict)
        service_info = {
            "service_name": deployment_class_arguments["project_id"]+"-cluster-ip",
            "service_port": cluster_ip_class_arguments_dict["port"],
        }
        add_to_ingress(
            startup_config_dict["networking_v1_api"], project_id, service_info)
    except Exception as e:
        print(
            f"Error in deploying project {project_id}")
        print(e)


def delete_model(startup_config_dict: dict, project_id: str):
    deployment_class_arguments["project_id"] = cluster_ip_class_arguments_dict["project_id"] = project_id
    try:
        delete_deployment_and_service(
            startup_config_dict["apps_v1"], startup_config_dict["core_v1"], project_id)
        service_info = {
            "service_name": deployment_class_arguments["project_id"]+"-cluster-ip",
            "service_port": cluster_ip_class_arguments_dict["port"],
        }
        remove_from_ingress(
            startup_config_dict["networking_v1_api"], project_id, service_info)
    except Exception as e:
        print(f"Error in deleting model {project_id}")
        print(e)


def recreate_ingress_rules(startup_config_dict: dict, projects_list: list):
    for project_id in projects_list:
        deployment_class_arguments["project_id"] = cluster_ip_class_arguments_dict["project_id"] = project_id
        service_info = {
            "service_name": deployment_class_arguments["project_id"]+"-cluster-ip",
            "service_port": cluster_ip_class_arguments_dict["port"],
        }
        add_to_ingress(
            startup_config_dict["networking_v1_api"], project_id, service_info)
