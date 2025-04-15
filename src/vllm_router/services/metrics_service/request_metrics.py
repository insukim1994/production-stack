from prometheus_client import Gauge

# New metrics per dashboard update
current_qps = Gauge("vllm:current_qps", "Current Queries Per Second", ["server"])
healthy_pods_total = Gauge(
    "vllm:healthy_pods_total", "Number of healthy vLLM pods", ["server"]
)
avg_latency = Gauge(
    "vllm:avg_latency", "Average end-to-end request latency", ["server"]
)
avg_itl = Gauge("vllm:avg_itl", "Average Inter-Token Latency", ["server"])
