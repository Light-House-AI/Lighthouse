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
                    default_backend=client.V1IngressBackend(
                        # TODO Create a deployment and cluster-ip for the default backend service
                        service=client.V1IngressServiceBackend(
                            name="classifier1-cluster-ip",
                            port=client.V1ServiceBackendPort(
                                number=8000
                            )
                        ),
                    )

                )
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
    def update_ingress_rules(api_client: client.NetworkingV1Api(), name: str, namespace: str, host_name: str, path: str, service_name: str, service_port: int):
        """
        This method will cause a downtime as all the previous services routes will be re-created along with the new one.
        If a request is made in-between this time, the request will fall back to the default backend service.
        """
        Ingress.__create_ingress_path__(path, service_name, service_port)
        try:
            body = client.V1Ingress(
                spec=client.V1IngressSpec(
                    rules=[
                        client.V1IngressRule(
                            host=host_name,
                            http=client.V1HTTPIngressRuleValue(
                                paths=Ingress.paths_list
                            )
                        )])
            )
            api_response = api_client.patch_namespaced_ingress(
                name, namespace, body, pretty=True,)
            # print(api_response)
            return True

        except Exception as e:
            print(f"Error in updating {name} rules ")
            print(e)
            return False

    @staticmethod
    def __create_ingress_path__(path: str, service_name: str, service_port: int):
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
            Ingress.paths_list.append(created_path)
            return True
        except Exception as e:
            print(f"Error in creating the path {path}")
            print(e)
            return False
