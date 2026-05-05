import random
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

from server import Server
from load_balancer import LoadBalancer


def generate_requests(num_requests=200):
    requests = []

    for i in range(num_requests):
        user_id = f"user_{random.randint(1, 20)}"

        requests.append({
            "request_id": i,
            "user_id": user_id
        })

    return requests


def process_request(load_balancer, request):
    server = load_balancer.choose_server(request)
    latency = server.handle_request()
    return server.name, latency


def run_test(load_balancer, requests, max_workers=30):
    latencies = []
    errors = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for request in requests:
            future = executor.submit(process_request, load_balancer, request)
            futures.append(future)

        for future in as_completed(futures):
            server_name, latency = future.result()

            if latency is None:
                errors += 1
            else:
                latencies.append(latency)

    return latencies, errors


def print_results(load_balancer, servers, latencies, errors, total_requests):
    algorithm_name = load_balancer.algorithm_name

    if latencies:
        avg_latency = statistics.mean(latencies)

        if len(latencies) >= 20:
            p95_latency = statistics.quantiles(latencies, n=20)[18]
        else:
            p95_latency = max(latencies)
    else:
        avg_latency = 0
        p95_latency = 0

    print("\n" + "=" * 60)
    print(f"EXPERIMENT RESULTS: {algorithm_name}")
    print("=" * 60)

    print(f"Total requests:       {total_requests}")
    print(f"Successful requests:  {len(latencies)}")
    print(f"Failed requests:      {errors}")
    print(f"Error rate:           {errors / total_requests:.2%}")

    print("\nOverall latency:")
    print(f"Average latency:      {avg_latency:.2f} ms")
    print(f"p95 latency:          {p95_latency:.2f} ms")

    print("\nServer load details:")

    for server in servers:
        request_share = server.total_requests / total_requests

        if server.latencies:
            server_avg_latency = statistics.mean(server.latencies)

            if len(server.latencies) >= 20:
                server_p95_latency = statistics.quantiles(server.latencies, n=20)[18]
            else:
                server_p95_latency = max(server.latencies)
        else:
            server_avg_latency = 0
            server_p95_latency = 0

        overload_status = "OK"
        if server.overload_count > 0:
            overload_status = "OVERLOADED"

        print(
            f"{server.name}: "
            f"{server.total_requests} requests "
            f"({request_share:.1%} traffic), "
            f"avg={server_avg_latency:.2f} ms, "
            f"p95={server_p95_latency:.2f} ms, "
            f"peak={server.peak_connections}/{server.capacity} connections, "
            f"overloads={server.overload_count}, "
            f"{overload_status}"
        )

    print("=" * 60)


def main():
    servers = [
        Server("server_A", base_latency=40, capacity=30, weight=3),
        Server("server_B", base_latency=60, capacity=20, weight=2),
        Server("server_C", base_latency=90, capacity=10, weight=1),
    ]

    requests = generate_requests(num_requests=600)

    load_balancer = LoadBalancer(servers)

    latencies, errors = run_test(
        load_balancer=load_balancer,
        requests=requests,
        max_workers=40
    )

    print_results(
        load_balancer=load_balancer,
        servers=servers,
        latencies=latencies,
        errors=errors,
        total_requests=len(requests)
    )


if __name__ == "__main__":
    main()