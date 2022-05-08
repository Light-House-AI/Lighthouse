from services.helpers import *
from services.startup import *
from k8s_client.ingress import Ingress


def run(model_id: str = None):
    is_first_time, startup_config_dict = startup()
    if is_first_time:
        # TODO startup_config_dict["secret_name"] has to be stored somewhere
        pass
    else:
        # TODO ingress paths list has to be loaded
        # Ingress.paths_list = [{'backend': {'resource': None,
        #                                    'service': {'name': 'classifier1-cluster-ip',
        #                                                'port': {'name': None, 'number': 8000}}},
        #                        'path': '/classifier1',
        #                        'path_type': 'Prefix'}]

        # TODO secret_name is to be loaded from the storage
        startup_config_dict["secret_name"] = "docker-registry-secret"
        if model_id:
            initiate_deployment(model_id=model_id,
                                startup_config_dict=startup_config_dict)
            # TODO ingress paths list has to be saved somewhere
        else:
            print("Send the model id you want to deploy! Exiting...")


def initiate_deployment(model_id: str, startup_config_dict: dict):
    deployment_envs_dict["AZURE_BLOB_NAME"] = model_id + PKL_EXTENTION
    deployment_class_arguments["model_id"] = cluster_ip_class_arguments_dict["model_id"] = model_id
    deployment_class_arguments["secret_name"] = startup_config_dict["secret_name"]
    deploy_model(startup_config_dict)


def deploy_model(startup_config_dict: dict):
    try:
        deployment_object, cluster_ip_object = create_deployment_and_service(
            startup_config_dict["apps_v1"], startup_config_dict["core_v1"], deployment_class_arguments, cluster_ip_class_arguments_dict)
        Ingress.update_ingress_rules(
            startup_config_dict["networking_v1_api"], name=INGRESS_NAME, namespace=CLUSTER_NAMESPACE, path="/" +
            deployment_class_arguments["model_id"],
            service_name=deployment_class_arguments["model_id"]+"-cluster-ip", service_port=cluster_ip_class_arguments_dict["port"])
    except Exception as e:
        print(
            f"Error in deploying model {deployment_class_arguments['model_id']}")
        print(e)
