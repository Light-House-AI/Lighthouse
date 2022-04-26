from kubernetes import client


class Deployment:
    def __init__(self, api: client.AppsV1Api(), model_id: str, namespace: str, replicas: int, image: str, env_vars: dict, secret_name: str):
        try:
            self.api = api
            self.model_id = model_id
            self.name = self.model_id + "-deployment"
            self.container_name = self.model_id + "-container"
            self.replicas = replicas
            self.image = image
            self.namespace = namespace
            self.env_vars = env_vars
            self.secret_name = secret_name
            self.container = None
            self.template = None
            self.spec = None
        except Exception as e:
            print(f"Error in creating the {model_id}-deployment")
            print(e)

    def __create_pod_template_container__(self):
        container = client.V1Container(
            name=self.container_name,
            image=self.image,
            image_pull_policy="Always",
            ports=[client.V1ContainerPort(container_port=8000)],
        )

        self.container = container

    def __create_template_section__(self):
        # TODO: Send environment variables to container
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"model": self.model_id}),
            spec=client.V1PodSpec(
                containers=[self.container], image_pull_secrets=[
                    client.V1LocalObjectReference(
                        name=self.secret_name)
                ]),
        )

        self.template = template

    def __create_spec_section__(self):
        spec = client.V1DeploymentSpec(
            replicas=self.replicas, template=self.template, selector={
                "matchLabels":
                {"model": self.model_id}})

        self.spec = spec

    def create_deployment(self):
        try:
            self.__create_pod_template_container__()
            self.__create_template_section__()
            self.__create_spec_section__()

            deployment_object = client.V1Deployment(
                api_version="apps/v1",
                kind="Deployment",
                metadata=client.V1ObjectMeta(name=self.name),
                spec=self.spec,
            )

            resp = self.api.create_namespaced_deployment(
                body=deployment_object, namespace=self.namespace
            )

            print(
                f"Deployment {resp.metadata.name} is created with status {resp.status}")
        except Exception as e:
            print(f"Error in creating the {self.name} deployment")
            print(e)
