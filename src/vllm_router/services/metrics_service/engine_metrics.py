from prometheus_client import Counter, Gauge, Histogram

# ---------------- vLLM Specific Metrics ----------------

cache_config_info = Gauge(
    "vllm:cache_config_info", "information of cache_config", ["test"]
)
num_requests_running = Gauge(
    "vllm:num_requests_running",
    "Number of requests currently running on GPU.",
    ["test"],
)
num_requests_waiting = Gauge(
    "vllm:num_requests_waiting",
    "Number of requests waiting to be processed.",
    ["test"],
)
num_requests_swapped = Gauge(
    "vllm:num_requests_swapped", "Number of requests swapped to CPU.", ["test"]
)
gpu_cache_usage_perc = Gauge(
    "vllm:gpu_cache_usage_perc",
    "GPU KV-cache usage. 1 means 100 percent usage.",
    ["test"],
)
cpu_cache_usage_perc = Gauge(
    "vllm:cpu_cache_usage_perc",
    "CPU KV-cache usage. 1 means 100 percent usage.",
    ["test"],
)
num_preemptions_total = Counter(
    "vllm:num_preemptions_total",
    "Cumulative number of preemption from the engine.",
    ["test"],
)
prompt_tokens_total = Counter(
    "vllm:prompt_tokens_total", "Number of prefill tokens processed.", ["test"]
)
generation_tokens_total = Counter(
    "vllm:generation_tokens_total", "Number of generation tokens processed.", ["test"]
)
request_success_total = Counter(
    "vllm:request_success_total",
    "Count of successfully processed requests.",
    ["test"],
)
avg_prompt_throughput_toks_per_s = Gauge(
    "vllm:avg_prompt_throughput_toks_per_s",
    "Average prefill throughput in tokens/s.",
    ["test"],
)
avg_generation_throughput_toks_per_s = Gauge(
    "vllm:avg_generation_throughput_toks_per_s",
    "Average generation throughput in tokens/s.",
    ["test"],
)
