import random
import threading


class LoadBalancer:
    def __init__(self, servers, algorithm_name="Default"):
        self.servers = servers
        self.algorithm_name = algorithm_name
        self.round_robin_index = 0
        self.lock = threading.Lock()

    def choose_server(self, request):
        """
        Change this function to test different load balancing algorithms.

        request looks like:
        {
            "request_id": 1,
            "user_id": "user_5"
        }
        """

        # TODO: Update your algorithm name!
        self.algorithm_name = "Default: First server always"

        # TODO: Implement your algorithm here!
        return self.servers[0]