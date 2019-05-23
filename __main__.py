import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from ServiceDeployment import ServiceDeployment


redisMaster = ServiceDeployment(
    "redis-master",
    {
        "image": "gcr.io/google_samples/gb-redisslave:v1",
        "ports": 6379
    }
)


redisReplica = ServiceDeployment(
    "redis-replica",
    {
        "image": "gcr.io/google_samples/gb-redisslave:v1",
        "ports": 6379
    }
)

frontend = ServiceDeployment(
    "frontend",
    {
        "replicas": 3,
        "image": "gcr.io/google-samples/gb-frontend:v4",
        "ports": 80,
        "serviceType": "LoadBalancer"
    }
)
