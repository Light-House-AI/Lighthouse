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
            print(self.env_vars)
        except Exception as e:
            print(f"Error in creating the {model_id}-deployment")
            print(e)

    def __create_pod_template_container__(self):
        container = client.V1Container(
            name=self.container_name,
            image=self.image,
            image_pull_policy="Always",
            ports=[client.V1ContainerPort(container_port=8000)],
            env=[
                client.V1EnvVar(
                    name=key, value=value
                ) for key, value in self.env_vars.items()
            ]
        )

        self.container = container

    def __create_template_section__(self):
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"model": self.model_id}),
            spec=client.V1PodSpec(
                containers=[self.container], image_pull_secrets=[
                    client.V1LocalObjectReference(
                        name=self.secret_name)],
            ),
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

    def delete_deployment(self):
        try:
            _ = self.api.delete_namespaced_deployment(
                name=self.name, namespace=self.namespace, propagation_policy="Foreground", grace_period_seconds=20)
            print(
                f"Deployment {self.name} is deleted with all its coressponding pods")

            return True

        except Exception as e:
            print(f"Error in deleting the {self.name} deployment")
            print(e)

            return False

    @staticmethod
    def get_deployments(api_client, namespace):
        try:
            resp = api_client.list_namespaced_deployment(
                namespace=namespace, pretty=True)

            print(f"Deployments in {namespace} namespace")
            for deployment in resp.items:
                print(f"{deployment.metadata.name}")

            return True

        except Exception as e:
            print(f"Error in getting the deployments")
            print(e)

            return False

    def get_pods(self, api_client: client.CoreV1Api):
        try:
            resp = api_client.list_namespaced_pod(pretty=True,
                                                  namespace=self.namespace, label_selector=f"model={self.model_id}")
            pods_counter = 1

            print(f"Pods in deployment {self.name}")
            for pod in resp.items:
                print(
                    f"Pod number {pods_counter} with name {pod.metadata.name} in deployment {self.name}")
                pods_counter += 1

            return True

        except Exception as e:
            print(f"Error in getting the pods of {self.name} deployment")
            print(e)

            return False