import random
import time
import threading


class Server:
    def __init__(self, name, base_latency, capacity, weight=1, failure_rate=0.0):
        self.name = name
        self.base_latency = base_latency
        self.capacity = capacity
        self.weight = weight
        self.failure_rate = failure_rate

        self.active_connections = 0
        self.peak_connections = 0
        self.overload_count = 0

        self.total_requests = 0
        self.errors = 0
        self.latencies = []

        self.lock = threading.Lock()

    def handle_request(self):
        with self.lock:
            self.total_requests += 1
            self.active_connections += 1

            if self.active_connections > self.peak_connections:
                self.peak_connections = self.active_connections

            current_connections = self.active_connections

            if current_connections > self.capacity:
                self.overload_count += 1

        overloaded = current_connections > self.capacity

        latency = random.gauss(self.base_latency, self.base_latency * 0.15)

        if overloaded:
            latency *= 2

        failure_chance = self.failure_rate

        if overloaded:
            failure_chance += 0.20

        failed = random.random() < failure_chance

        time.sleep(latency / 1000)

        with self.lock:
            self.active_connections -= 1

            if failed:
                self.errors += 1
                return None

            latency = max(latency, 1)
            self.latencies.append(latency)

        return latency