import base64


def encode_base64(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def create_docker_config_json_file_string(server, base64_encoded_token):
    docker_config_json_string = "{\"auths\":{\"%s\":{\"auth\":\"%s\"}}}" % (server,
                                                                            base64_encoded_token)

    return docker_config_json_string
