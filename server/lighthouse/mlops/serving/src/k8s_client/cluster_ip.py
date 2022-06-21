from kubernetes import client


class ClusterIP:
    def __init__(self, api: client.CoreV1Api(), cluster_ip_class_arguments_dict: dict):
        self.api = api
        self.project_id = cluster_ip_class_arguments_dict["project_id"]
        self.name = cluster_ip_class_arguments_dict["project_id"] + \
            "-cluster-ip"
        self.namespace = cluster_ip_class_arguments_dict["namespace"]
        self.port = cluster_ip_class_arguments_dict["port"]
        self.target_port = cluster_ip_class_arguments_dict["target_port"]

    def create_cluster_ip(self):
        try:
            body = client.V1Service(
                api_version="v1",
                kind="Service",
                metadata=client.V1ObjectMeta(
                    name=self.name,
                    labels={"status": "user-created-cluster-ip"},
                ),
                spec=client.V1ServiceSpec(
                    type="ClusterIP",
                    selector={"project": self.project_id},
                    ports=[client.V1ServicePort(
                        port=self.port,
                        target_port=self.target_port
                    )],
                )
            )

            self.api.create_namespaced_service(
                namespace=self.namespace, body=body)

            print(f"Cluster IP {self.name} is created")
            return True

        except Exception as e:
            print(
                f"Error in creating the {self.name}. Check the sent parameters")
            print(e)
            return False

    @staticmethod
    def get_cluster_ips(api_client: client.CoreV1Api(), namespace: str):
        try:
            resp = api_client.list_namespaced_service(
                namespace=namespace, label_selector='status=user-created-cluster-ip', pretty=True)

            print(f"Services in {namespace} namespace")
            for service in resp.items:
                print(f"{service.metadata.name}")

            return resp.items

        except Exception as e:
            print(f"Error in getting the services")
            print(e)

    @staticmethod
    def delete_cluster_ip(api_client: client.CoreV1Api(), name: str, namespace: str):
        try:
            api_client.delete_namespaced_service(
                name=name, namespace=namespace, grace_period_seconds=10, propagation_policy="Foreground")
            print(f"Cluster IP {name} is deleted")
            return True
        except Exception as e:
            print(f"Error in deleting the {name}.")
            print(e)
            return False
