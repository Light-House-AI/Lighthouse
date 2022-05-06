from services.helpers import *
from services.startup import *


def run():
    apps_v1, core_v1, networking_v1_api, secret_name, ingress_object = startup()
    # ? TEST SCOPE
    deployment_class_arguments["secret_name"] = secret_name
    deployment_object, cluster_ip_object = create_deployment_and_service(
        apps_v1, core_v1, deployment_class_arguments, cluster_ip_class_arguments_dict)
    Ingress.update_ingress_rules(
        api_client=networking_v1_api, name=INGRESS_NAME, namespace=CLUSTER_NAMESPACE, path="/" +
        deployment_class_arguments["model_id"],
        service_name=deployment_class_arguments["model_id"]+"-cluster-ip", service_port=cluster_ip_class_arguments_dict["port"])
