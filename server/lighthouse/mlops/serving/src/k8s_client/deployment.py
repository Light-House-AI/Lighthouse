from kubernetes import client


class Deployment:
    def __init__(self, api: client.AppsV1Api(), deployment_class_arguments: dict):
        try:
            self.api = api
            self.project_id = deployment_class_arguments["project_id"]
            self.model_id = deployment_class_arguments["model_id"]
            self.challenger_model_id = deployment_class_arguments["challenger_model_id"]
            self.name = self.project_id + "-deployment"
            self.container_name = self.project_id + "-container"
            self.replicas = deployment_class_arguments["replicas"]
            self.image = deployment_class_arguments["image"]
            self.namespace = deployment_class_arguments["namespace"]
            self.env_vars = deployment_class_arguments["env_vars"]
            self.secret_name = deployment_class_arguments["secret_name"]
            self.container = None
            self.template = None
            self.spec = None
        except Exception as e:
            print(f"Error in creating the {self.project_id}-deployment")
            print(e)

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
                f"Deployment {resp.metadata.name} is created.")
            return True

        except Exception as e:
            print(f"Error in creating the {self.name} deployment")
            print(e)
            return False

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
            metadata=client.V1ObjectMeta(labels={"project": self.project_id}),
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
                {"project": self.project_id}})

        self.spec = spec

    @staticmethod
    def delete_deployment(api_client: client.AppsV1Api(), name: str, namespace: str):
        try:
            api_client.delete_namespaced_deployment(
                name=name, namespace=namespace, propagation_policy="Foreground", grace_period_seconds=10)
            print(
                f"Deployment {name} is deleted with all its corresponding pods")
            return True

        except Exception as e:
            print(f"Error in deleting the {name} deployment")
            print(e)
            return False

    @staticmethod
    def get_deployments(api_client: client.AppsV1Api(), namespace: str):
        try:
            resp = api_client.list_namespaced_deployment(
                namespace=namespace, pretty=True)

            print(f"Deployments in {namespace} namespace")
            for deployment in resp.items:
                print(f"{deployment.metadata.name}")

            return resp.items

        except Exception as e:
            print(f"Error in getting the deployments")
            print(e)

# TODO check this fn

    @staticmethod
    def get_pods(api_client: client.CoreV1Api, model_id: str, namespace: str):
        # deployment_name = project_id+"-deployment"
        try:
            resp = api_client.list_namespaced_pod(pretty=True,
                                                  namespace=namespace, label_selector=f"model={model_id}")
            pods_counter = 1

            print(f"Pods in deployment {model_id}-deployment")
            for pod in resp.items:
                print(
                    f"Pod number {pods_counter} with name {pod.metadata.name} in deployment {model_id}-deployment")
                pods_counter += 1

            return True

        except Exception as e:
            print(f"Error in getting the pods of {model_id}-deployment")
            print(e)
            return False
