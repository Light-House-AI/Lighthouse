from kubernetes import client


class Ingress:
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
                            # TODO Add host
                            http=client.V1HTTPIngressRuleValue(
                                paths=[
                                    client.V1HTTPIngressPath(
                                        path="/?(.*)",
                                        path_type="Prefix",
                                        backend=client.V1IngressBackend(
                                            service=client.V1IngressServiceBackend(
                                                name="classifier1-cluster-ip",
                                                port=client.V1ServiceBackendPort(
                                                    number=8000
                                                )
                                            )
                                        )
                                    )
                                ]
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
