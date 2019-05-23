import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service


class ServiceDeployment(pulumi.ComponentResource):

    def __init__(self, name, args, opts=None):
        super().__init__("ServiceDeployment", name, {}, opts)
        self.name = name
        self.labels = {"app": name}
        self.deployment = Deployment(
            name,
            spec={
                "selector": {
                    "match_labels": self.labels
                },
                "replicas": args.get("replicas", 1),
                "template": {
                    "metadata": {
                        "labels": self.labels
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": self.name,
                                "image": args.get("image")
                            }
                        ]
                    }
                }
            }
        )

        self.service = Service(
            name,
            spec={
                "type": args.get("serviceType", "ClusterIP"),
                "ports": [
                    {
                        "port": args.get("port"),
                        "targetPort": args.get("port"),
                        "protocol": args.get("protocol", "TCP")
                    }
                ],
                "selector": self.labels
            }
        )

        pulumi.export(
            "frontendIp",
            self.service.status["load_balancer"]["ingress"][0]["hostname"])
