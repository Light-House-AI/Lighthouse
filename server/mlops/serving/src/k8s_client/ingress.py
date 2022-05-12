from kubernetes import client


class Ingress:
    paths_list = []

    def __init__(self, api_client: client.NetworkingV1Api(), name: str, namespace: str, ingress_class: str):
        self.api_client = api_client
        self.name = name
        self.namespace = namespace
        self.ingress_class = ingress_class

    def create_ingress(self):
        try:
            body = client.V1Ingress(
                api_version="networking.k8s.io/v1",
                kind="Ingress",
                metadata=client.V1ObjectMeta(
                    name=self.name,
                    annotations={
                        "kubernetes.io/ingress.class": self.ingress_class,
                        "nginx.ingress.kubernetes.io/use-regex": "true",
                        "nginx.ingress.kubernetes.io/rewrite-target": "/$1"
                    },
                ),
                spec=client.V1IngressSpec(
                    rules=[
                        client.V1IngressRule(
                            http=client.V1HTTPIngressRuleValue(
                                paths=Ingress.paths_list
                            )
                        )])
            )
            self.api_client.create_namespaced_ingress(
                namespace=self.namespace,
                body=body
            )
            print(f"Ingress {self.name} is created")
            return True

        except Exception as e:
            print(f"Error in creating the ingress {self.name}")
            print(e)
            return False

    @staticmethod
    def update_ingress_rules(api_client: client.NetworkingV1Api(), name: str, namespace: str):
        try:
            body = client.V1Ingress(
                spec=client.V1IngressSpec(
                    rules=[
                        client.V1IngressRule(
                            http=client.V1HTTPIngressRuleValue(
                                paths=Ingress.paths_list
                            )
                        )])
            )
            api_response = api_client.patch_namespaced_ingress(
                name, namespace, body, pretty=True,)
            return True

        except Exception as e:
            print(f"Error in updating {name} rules ")
            print(e)
            return False

    @staticmethod
    def create_ingress_path(path: str, service_name: str, service_port: int):
        try:
            created_path = client.V1HTTPIngressPath(
                path=path,
                path_type="Prefix",
                backend=client.V1IngressBackend(
                    service=client.V1IngressServiceBackend(
                        name=service_name,
                        port=client.V1ServiceBackendPort(
                            number=service_port
                        )
                    )
                )
            )
            return created_path
        except Exception as e:
            print(f"Error in creating the path {path}")
            print(e)
            return None

    @staticmethod
    def get_ingresses(api_client: client.NetworkingV1Api(), namespace: str):
        try:
            ingresses_list = api_client.list_namespaced_ingress(
                namespace=namespace,
                pretty=True,
            )
            print(f"The ingresses in the {namespace} namespace are:")

            for ingress in ingresses_list.items:
                print(ingress.metadata.name)

            return ingresses_list.items

        except Exception as e:
            print(f"Error in getting the ingresses")
            print(e)
            return None

    @staticmethod
    def delete_ingress(api_client: client.NetworkingV1Api(), namespace: str, name: str):
        try:
            api_client.delete_namespaced_ingress(
                name=name,
                namespace=namespace,
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground", grace_period_seconds=20
                ),
                pretty=True,
            )
            print(f"Ingress {name} is deleted successfully")
            return True

        except Exception as e:
            print(f"Error in deleting the ingress")
            print(e)
            return False
