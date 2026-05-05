# Load Balancer Workshop

This workshop is a beginner-friendly simulation of how load balancers distribute traffic across backend servers.

Participants act as backend engineers testing different load balancing algorithms under realistic traffic conditions. Instead of only learning theory, you will run experiments, change the load balancing logic, and compare system performance using metrics like latency, error rate, server utilization, and overload count.

## Workshop Goal

By the end of this workshop, you should understand:

- What a load balancer does
- How different load balancing algorithms route traffic
- Why real systems behave differently than theory
- How latency, failures, and server capacity affect performance
- How engineers make tradeoffs when designing production systems

## Repository Structure

```text
load-balancer-workshop/
│
├── main.py              # Runs the simulation and prints results
├── load_balancer.py     # File participants edit during the workshop
├── server.py            # Defines server behavior, latency, failures, and overloads
└── README.md
```

## Basic Workflow

1. Open `load_balancer.py`
2. Edit the `choose_server()` function
3. Save the file
4. Run the simulation from `main.py`
```bash
python main.py
``` 
6. Compare the printed metrics
7. Try another algorithm


