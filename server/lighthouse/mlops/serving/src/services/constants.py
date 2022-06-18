# Constants file
# * GENERAL CONSTANTS
PKL_EXTENSION = ".pkl"
IMAGE_NAME = "ghcr.io/light-house-ai/model-wrapper:latest"
IMAGE_SECRET_NAME = "ghcr-registry-secret"
IMAGE_SERVER = "ghcr.io"
CONTAINER_NAME = "models"
CLUSTER_NAMESPACE = "default"
# * CLUSTER_IP CONSTANTS
DEFAULT_CLUSTER_IP_PORT = 8000
DEFAULT_CLUSTER_IP_TARGET_PORT = 8000
# * INGRESS CONSTANTS
INGRESS_NAME = "models-ingress"
INGRESS_CLASS = "nginx"
# * DEFAULT DEPLOYMENT CONSTANTS
DEFAULT_PROJECT_ID = "default"
DEFAULT_IMAGE_NAME = "ghcr.io/light-house-ai/lighthouse-client:latest"
