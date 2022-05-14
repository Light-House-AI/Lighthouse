from kubernetes import client
from k8s_client.helpers import encode_base64, create_docker_config_json_file_string


class Secret:
    def __init__(self, api: client.CoreV1Api(), name: str, username: str, password: str, server: str, namespace: str):
        try:
            self.api = api
            self.name = name
            self.server = server
            self.namespace = namespace
            self.base64_encoded_token = encode_base64(
                "%s:%s" % (username, password))
            self.encoded_docker_config_json_string = encode_base64(create_docker_config_json_file_string(self.server,
                                                                                                         self.base64_encoded_token))
        except Exception as e:
            print(f"Error in sent parameters for {name} secret")
            print(e)

    def create_docker_registry_secret(self):
        try:
            secret_object = client.V1Secret(
                api_version="v1",
                kind="Secret",
                metadata=client.V1ObjectMeta(
                    name=self.name, namespace=self.namespace),
                type="kubernetes.io/dockerconfigjson",
                data={
                    ".dockerconfigjson": self.encoded_docker_config_json_string
                }
            )

            resp = self.api.create_namespaced_secret(
                namespace=self.namespace, body=secret_object)

            print(f"Secret '{resp.metadata.name}' is created")
            return True

        except Exception as e:
            print(f"Error in creating secret '{self.name}'")
            print(e)
            return False
